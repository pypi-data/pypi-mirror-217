from typing import Any

from requests import Session, Response

import logging

log = logging.getLogger(__name__)


class EventixClientSession(Session):
    def __init__(self, base_url: str = None) -> None:
        self.base_url = base_url
        super().__init__()

    def request(
        self,
        method: str | bytes,
        url: str | bytes,
        *args,
        **kwargs
    ) -> Response:  # pragma: no cover
        return super().request(
            method,
            f"{self.base_url}{url}",
            *args,
            **kwargs
        )


class EventixClient:
    interface: Any | None = EventixClientSession()
    namespace: str | None = None

    @classmethod
    def set_base_url(cls, base_url):
        if isinstance(cls.interface, EventixClientSession):
            log.info(f"Setting EventixClient base_url: {base_url}")
            cls.interface.base_url = base_url
