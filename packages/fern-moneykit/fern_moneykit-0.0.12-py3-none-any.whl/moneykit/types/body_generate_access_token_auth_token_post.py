# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ..core.datetime_utils import serialize_datetime


class BodyGenerateAccessTokenAuthTokenPost(pydantic.BaseModel):
    grant_type: typing.Optional[str] = pydantic.Field(
        description=("Token grant type. Only `client_credentials` supported.\n")
    )
    scope: typing.Optional[str] = pydantic.Field(
        description=(
            "Actions to be allowed for this token, given as one or more strings separated by spaces.\n"
            "            If omitted, all actions allowed for your application will be granted to this token.\n"
        )
    )
    client_id: typing.Optional[str] = pydantic.Field(description=("Your application's MoneyKit client ID.\n"))
    client_secret: typing.Optional[str] = pydantic.Field(description=("Your application's MoneyKit client secret.\n"))

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        json_encoders = {dt.datetime: serialize_datetime}
