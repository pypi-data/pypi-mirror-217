import logging

from fastapi import APIRouter

from eventix.functions.tools import metrics

log = logging.getLogger(__name__)

router = APIRouter(tags=["metrics"])


@router.get("/metrics")
async def metrics_get():
    return metrics()
