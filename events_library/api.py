"""Generic API class."""
import typing

from django.conf import settings
from requests import Request, RequestException, Session, HTTPError
from rest_framework.renderers import JSONRenderer


class BaseApi:
    """Base class for serving different APIs."""

    def __init__(self, domain: str = None) -> None:
        """Initialize requests session."""
        self.session = Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
        })
        self.domain = domain or settings.DOMAIN_NAME

    def send_request(
        self,
        path: str,
        data: typing.Dict,
        raise_exception: bool = True,
    ) -> typing.Tuple[int, bool]:
        """Send request function."""

        req = Request(
            method='POST',
            url=f'https://{self.domain}/{path}',
            data=JSONRenderer().render(data),
            headers={
                'Token': settings.JWT_AUTH['SERVICE_SECRET_TOKEN']
            },
        )

        retries = 0
        max_retries = 1
        prepared_req = self.session.prepare_request(req)

        while (retries < max_retries):
            try:
                resp = self.session.send(prepared_req)
                if raise_exception:
                    resp.raise_for_status()

                return retries, True

            except (HTTPError, RequestException):
                retries += 1

        return max_retries, False
