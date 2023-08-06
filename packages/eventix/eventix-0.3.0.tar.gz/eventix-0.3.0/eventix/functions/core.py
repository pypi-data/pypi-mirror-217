import contextlib
import contextvars
import functools
import logging
import os
from typing import Callable

from eventix.functions.task_scheduler import TaskScheduler
from eventix.pydantic.task import TaskModel

log = logging.getLogger(__name__)


class EventflowTaskBase(object):
    pass


namespace_context_var = contextvars.ContextVar('namespace_context_var', default=None)


@contextlib.contextmanager
def namespace_provider(namespace: str):
    # noinspection PyTypeChecker
    token = namespace_context_var.set(namespace)
    yield
    namespace_context_var.reset(token)


@contextlib.contextmanager
def namespace_context():
    # noinspection PyTypeChecker
    namespace = namespace_context_var.get()
    if namespace is None:
        namespace = os.environ.get("EVENTFLOW_TASK_NAMESPACE", "default")
    yield namespace


worker_id_context_var = contextvars.ContextVar('worker_id_context_var', default=None)


@contextlib.contextmanager
def worker_id_provider(worker_id: str):
    # noinspection PyTypeChecker
    token = worker_id_context_var.set(worker_id)
    yield
    worker_id_context_var.reset(token)


@contextlib.contextmanager
def worker_id_context():
    # noinspection PyTypeChecker
    worker_id = worker_id_context_var.get()
    if worker_id is None:
        worker_id = os.environ.get("EVENTFLOW_TASK_WORKER_ID", "default")
    yield worker_id


def task(result: bool = True, unique_key_generator: Callable = None):
    # parameters suggested:
    #
    # result: bool , wether to store or not to store results
    # unique_uid: ....  having a unique id, which leads to update the task if it is rescheduled.

    # retry: bool, wether to retry failed tasks
    # max_retry: int, maximum retries default 5 ... each retry doubles the time to wait, starting with 30 sec

    is_unique = unique_key_generator is not None

    def inner(f):
        class EventflowTask(EventflowTaskBase):
            def __init__(self):
                self.func = f
                self.func_name = f.__name__

            @functools.wraps(f)
            def delay(self, *args, _priority: int | None = 0, **kwargs):
                # priority has to be negated, needed for fixing ascending sort order

                tm = self.make_task_model(args, kwargs, priority=_priority * -1)
                # log.debug(f"scheduling {self.func.__name__} info: {tm.json()}")
                tm = TaskScheduler.schedule(tm)
                return tm

            @functools.wraps(f)
            def run(self, *args, **kwargs):
                return self.func(*args, **kwargs)

            def make_task_model(self, args, kwargs, priority) -> TaskModel:
                params = dict(
                    task=self.func_name,
                    args=args,
                    kwargs=kwargs,
                    priority=priority
                )
                if is_unique:
                    unique_key = unique_key_generator(*args, **kwargs)
                    params |= dict(unique_key=unique_key)

                return TaskModel.parse_obj(params)

        return EventflowTask()

    return inner


