from eventix.functions.core import task
from eventix.functions.task import task_clean_expired_workers


@task()
def task_cleanup_worker():
    task_clean_expired_workers()


@task()
def task_cleanup_results():
    pass
