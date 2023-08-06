import contextlib
from typing import List, Type

import pydash
from fastapi import HTTPException


@contextlib.contextmanager
def raise_errors(r, exceptions: List[Type[Exception]]):
    exceptions_by_class = {e.__name__: e for e in exceptions}
    if r.status_code == 200:
        yield r
    else:
        json = r.json()
        detail = pydash.get(json, 'detail', json)
        error_class = pydash.get(detail, 'error_class')
        payload = pydash.get(detail, 'error_payload', {})
        if error_class in exceptions_by_class:
            e = exceptions_by_class[error_class](**payload)
            raise e
        # backend errors
        raise HTTPException(status_code=r.status_code, detail=detail)
