from __future__ import annotations

import importlib
import logging
import os
import sys
import time
from typing import List

import dotenv
from pydantic_db_backend.utils import utcnow

from eventix.exceptions import TaskNotRegistered, backend_exceptions
from eventix.functions.core import EventflowTaskBase, namespace_context, worker_id_context, namespace_provider
from eventix.functions.errors import raise_errors
from eventix.functions.eventix_client import EventixClient
from eventix.functions.task import task_set_error, task_set_result
from eventix.pydantic.task import TaskModel

log = logging.getLogger(__name__)


class TaskWorker(EventixClient):
    _wait_interval = 10
    _tasks = {}
    namespace: str = None

    @classmethod
    def setup_logging(cls, without_time: bool = False, level: int = logging.INFO):
        if without_time:
            f = "[%(levelname)8s] %(message)s"
        else:
            f = "%(asctime)s [%(levelname)s] %(message)s"
        logging.basicConfig(
            level=level,
            format=f,
            handlers=[
                logging.StreamHandler()
            ]
        )

    @classmethod
    def config(cls, config: dict):

        base_url = os.environ.get("EVENTIX_URL", "")
        if base_url == "":
            log.error("No EVENTIX_URL set.")
            sys.exit()

        cls.set_base_url(base_url)

        if "register_tasks" in config:
            cls.register_tasks(config['register_tasks'])

        if "namespace" in config:
            cls.namespace = config['namespace']

        namespace = os.environ.get("EVENTIX_NAMESPACE", "")
        if namespace != "":
            cls.namespace = namespace

    @classmethod
    def register_tasks(cls, paths=List[str]):
        log.info("registering tasks...")
        # noinspection PyTypeChecker
        for path in paths:
            try:
                imported_module = importlib.import_module(path)
                for f in filter(
                    lambda x: isinstance(x, EventflowTaskBase),
                    [getattr(imported_module, x) for x in dir(imported_module)]
                ):
                    log.info(f"registered '{f.func_name}' from {path}")
                    cls._tasks[f.func_name] = f
            except ImportError as e:
                print(e)

    @classmethod
    def task_next_scheduled(cls) -> TaskModel | None:
        with namespace_context() as namespace:
            with worker_id_context() as worker_id:
                params = dict(
                    worker_id=worker_id,
                    namespace=namespace
                )
                r = cls.interface.get(f'/task/next_scheduled', params=params)
                if r.status_code == 200:
                    tm = TaskModel.parse_raw(r.content)
                    return tm
                else:
                    return None

    # with raise_errors(r):
    #     return TaskModel.parse_raw(r.content)

    @classmethod
    def listen(cls, endless=True):
        log.info("Start listening...")
        while True:
            log.info("Looking for tasks...")
            t = cls.task_next_scheduled()
            if t is not None:
                cls.execute_task(t)
            else:
                log.info(f"Nothing to do... waiting {cls._wait_interval}s")
                if not endless:
                    return
                time.sleep(cls._wait_interval)

    @classmethod
    def execute_task(cls, task: TaskModel):
        try:
            log.info(f"Executing task: {task.task} uid: {task.uid} ...")

            if task.task not in cls._tasks:
                raise TaskNotRegistered(task=task.task)  # Task not registered in worker

            f = cls._tasks[task.task]
            r = f.run(*task.args, **task.kwargs)
            if task.store_result:
                task_set_result(task, r)

        except TaskNotRegistered as e:
            log.exception(e)
            task_set_error(
                task,
                TaskNotRegistered(task=task.task)
            )

        except Exception as e:
            log.exception(e)
            task_set_error(task, e)

        finally:
            cls.task_write_back(task)

    @classmethod
    def task_write_back(cls, task: TaskModel) -> TaskModel | None:
        try:

            if task.expires is not None and task.expires < utcnow():  # gammel
                # if task is already expired, delete it instead of updating
                r = cls.interface.delete(f'/task/{task.uid}')
                return None
            else:
                # task not yet expired.... update
                r = cls.interface.put(f'/task/{task.uid}', data=task.json())

            with raise_errors(r, backend_exceptions):
                if r.status_code == 200:
                    tm = TaskModel.parse_raw(r.content)
                    return tm

        except Exception as e:
            log.error("Exception raised when calling eventix")
            log.exception(e)
            log.error("Exception used this task info")
            log.error(task.json())

        return None

    @classmethod
    def load_env(cls):
        dotenv.load_dotenv(".env.local")

    def __init__(self, config: dict) -> None:
        self.setup_logging()
        self.load_env()
        self.config(config)

    def start(self, endless: bool = True):
        log.info(f"Using namespace: {self.namespace}")
        with namespace_provider(self.namespace):
            self.listen(endless)
