# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ..core.datetime_utils import serialize_datetime
from .link_products import LinkProducts
from .public_link_error import PublicLinkError
from .public_link_state import PublicLinkState


class LinkCommon(pydantic.BaseModel):
    link_id: str = pydantic.Field(description=("The unique ID for this link.\n"))
    institution_id: str = pydantic.Field(description=("The unique ID for the institution this link is connected to.\n"))
    institution_name: str = pydantic.Field(description=("The institution name this link is connected to.\n"))
    state: PublicLinkState = pydantic.Field(
        description=(
            "The current state of this link.  Links that are not yet connected,\n"
            "        or which require reconnection, will be in one of the non-connected states.\n"
        )
    )
    error_code: typing.Optional[PublicLinkError] = pydantic.Field(
        description=(
            "The type of error, if the link is in the `error` state.  See <a href=/pages/errors>Errors</a> for an explanation of error codes.\n"
        )
    )
    last_synced_at: typing.Optional[str] = pydantic.Field(
        description=("An ISO-8601 timestamp indicating the last time that the account was updated.\n")
    )
    tags: typing.Optional[typing.List[str]] = pydantic.Field(
        description=("Arbitrary strings used to describe this link.\n")
    )
    products: LinkProducts = pydantic.Field(description=("The granted products available for this link.\n"))

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        json_encoders = {dt.datetime: serialize_datetime}
