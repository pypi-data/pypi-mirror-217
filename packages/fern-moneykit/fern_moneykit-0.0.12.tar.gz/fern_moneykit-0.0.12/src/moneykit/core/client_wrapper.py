# This file was auto-generated by Fern from our API Definition.

import typing

import httpx

from ..types.supported_version import SupportedVersion


class BaseClientWrapper:
    def __init__(
        self,
        *,
        moneykit_version: typing.Optional[SupportedVersion] = None,
        token: typing.Union[str, typing.Callable[[], str]],
    ):
        self._moneykit_version = moneykit_version
        self._token = token

    def get_headers(self) -> typing.Dict[str, str]:
        headers: typing.Dict[str, str] = {}
        if self._moneykit_version is not None:
            headers["moneykit-version"] = self._moneykit_version
        headers["Authorization"] = f"Bearer {self._get_token()}"
        return headers

    def _get_token(self) -> str:
        if isinstance(self._token, str):
            return self._token
        else:
            return self._token()


class SyncClientWrapper(BaseClientWrapper):
    def __init__(
        self,
        *,
        moneykit_version: typing.Optional[SupportedVersion] = None,
        token: typing.Union[str, typing.Callable[[], str]],
        httpx_client: httpx.Client,
    ):
        super().__init__(moneykit_version=moneykit_version, token=token)
        self.httpx_client = httpx_client


class AsyncClientWrapper(BaseClientWrapper):
    def __init__(
        self,
        *,
        moneykit_version: typing.Optional[SupportedVersion] = None,
        token: typing.Union[str, typing.Callable[[], str]],
        httpx_client: httpx.AsyncClient,
    ):
        super().__init__(moneykit_version=moneykit_version, token=token)
        self.httpx_client = httpx_client
