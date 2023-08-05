# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ..core.datetime_utils import serialize_datetime
from .country import Country
from .link_permissions import LinkPermissions
from .products_settings import ProductsSettings
from .provider import Provider


class LinkSessionSettingOverrides(pydantic.BaseModel):
    providers: typing.Optional[typing.List[Provider]] = pydantic.Field(
        description=(
            "If provided, restricts the available institutions to those supported\n"
            "            by **any** of these providers.\n"
        )
    )
    link_permissions: typing.Optional[LinkPermissions] = pydantic.Field(
        description=(
            "A set of permissions that the user will be prompted to grant. **Required** permissions will\n"
            "            restrict the available institutions list to those which support that type of data.  The data you\n"
            "            will be able to fetch from the link is limited to the granted permissions set.\n"
        )
    )
    products: typing.Optional[ProductsSettings] = pydantic.Field(
        description=("If provided, configures what institutions are available and how data should be fetched.\n")
    )
    countries: typing.Optional[typing.List[Country]] = pydantic.Field(
        description=("Restricts the available institutions to those in **any** of these countries.\n")
    )

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        json_encoders = {dt.datetime: serialize_datetime}
