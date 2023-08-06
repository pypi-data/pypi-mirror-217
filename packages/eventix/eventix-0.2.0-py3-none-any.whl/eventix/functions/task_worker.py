import importlib
import logging
import time
from typing import List

from eventix.exceptions import TaskNotRegistered, backend_exceptions
from eventix.functions.core import EventflowTaskBase, namespace_context, worker_id_context
from eventix.functions.eventflow_client import EventflowClient
from eventix.functions.task import task_set_error
from eventix.pydantic.task import TaskModel
from pydantic_db_backend.utils import utcnow
from webexception.webexception import raise_errors

log = logging.getLogger(__name__)


class TaskWorker(EventflowClient):
    _wait_interval = 10
    _tasks = {}

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
        while True:
            log.info("Start listening...")
            t = cls.task_next_scheduled()
            if t is not None:
                pass
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
                task.result = r

        except TaskNotRegistered as e:
            log.exception(e)
            task_set_error(
                task,
                TaskNotRegistered(task=task.task)
            )

        except Exception as e:
            task_set_error(task, e)

        finally:
            cls.task_write_back(task)

    @classmethod
    def task_write_back(cls, task: TaskModel) -> TaskModel | None:
        try:

            if task.expires < utcnow():
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
            log.error("Exception happend calling eventflow")
            log.exception(e)
            log.error("Exception used this task info")
            log.error(task.json())

        return None
