"""Generic API class."""
import enum
import typing

import requests
from django.conf import settings


@enum.unique
class HttpMethod(enum.Enum):
    """Basic HTTP methods."""

    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'


class BaseApi:
    """Base class for serving different APIs."""

    domain = settings.DOMAIN_NAME

    class Error(Exception):
        """Generic error class."""

        pass

    def __init__(self, domain: str = None) -> None:
        """Initialize requests session."""
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
        })
        self.domain = domain or self.domain

    @property
    def root_url(self) -> str:
        """Return SD base path."""
        return f'https://{self.domain}/'

    def send_request(
            self, *,
            method: HttpMethod,
            path: str,
            data: typing.Union[str, bytes] = None,
            headers: typing.Dict[str, str] = None,
            raise_exception: bool = False,
    ) -> requests.Response:
        """Send request function."""
        req = requests.Request(
            method=method.value,
            url=f'{self.root_url}{path}',
            headers=headers,
            data=data,
        )
        prepared_req = self.session.prepare_request(req)

        resp = self.session.send(prepared_req)
        if raise_exception:
            resp.raise_for_status()
        return resp
