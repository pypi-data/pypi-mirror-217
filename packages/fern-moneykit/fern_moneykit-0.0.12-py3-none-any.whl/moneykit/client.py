import httpx
import pydantic
import time
import typing
import urllib.parse

from .environment import BaseMoneyKitEnvironment
from .types.supported_version import SupportedVersion
from .base_client import BaseMoneyKit
from .base_client import AsyncBaseMoneyKit
from .types.generate_access_token_response import GenerateAccessTokenResponse
from .core.api_error import ApiError

class MoneyKit(BaseMoneyKit):
    def __init__(
        self,
        *,
        environment: BaseMoneyKitEnvironment = BaseMoneyKitEnvironment.PRODUCTION,
        moneykit_version: typing.Optional[SupportedVersion] = None,
        client_id: str,
        client_secret: str,
        timeout: typing.Optional[float] = 60
    ):
        super().__init__(
            environment=environment, 
            moneykit_version=moneykit_version, 
            timeout=timeout,
            token=MoneyKitTokenSupplier(
                environment=environment, client_id=client_id, client_secret=client_secret)
        )

class AsyncMoneyKit(AsyncBaseMoneyKit):
    def __init__(
        self,
        *,
        environment: BaseMoneyKitEnvironment = BaseMoneyKitEnvironment.PRODUCTION,
        moneykit_version: typing.Optional[SupportedVersion] = None,
        client_id: str,
        client_secret: str,
        timeout: typing.Optional[float] = 60
    ):
        super().__init__(
            environment=environment, 
            moneykit_version=moneykit_version, 
            timeout=timeout,
            token=MoneyKitTokenSupplier(
                environment=environment, client_id=client_id, client_secret=client_secret)
        )


class MoneyKitTokenSupplier(): 
    def __init__(self, *, environment: BaseMoneyKitEnvironment, client_id: str, client_secret: str): 
        self.environment = environment
        self.client_id = client_id
        self.client_secret = client_secret
        self.token: typing.Optional[str] = None
        self.expiration_time: typing.Optional[float] = time.time()
        
    def __call__(self) -> str:
        if self.token is None \
            or (self.expiration_time is not None and time.time() > self.expiration_time): 
            response = httpx.request(
                "POST",
                urllib.parse.urljoin(f"{self.environment.value}/", "auth/token"),
                auth=httpx.BasicAuth(self.client_id, self.client_secret),
                timeout=60,
            )
            if 200 <= response.status_code < 300:
                parsed_response = pydantic.parse_obj_as(GenerateAccessTokenResponse, response.json())
                self.expiration_time = time.time() + parsed_response.expires_in
                self.token = parsed_response.access_token
                return self.token
            else: 
                raise ApiError(status_code=response.status_code, 
                               body=f"Request to get Moneykit access token failed: {response.text}")
        else:
            return self.token

