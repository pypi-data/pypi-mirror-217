# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ..core.datetime_utils import serialize_datetime
from .account_balances import AccountBalances
from .account_numbers import AccountNumbers
from .account_type import AccountType


class AccountWithAccountNumbers(pydantic.BaseModel):
    account_id: str = pydantic.Field(
        description=(
            "MoneyKit's unique ID for the account.\n"
            "        <p>The `account_id` is distinct from the institution's account number.  For accounts that may change account\n"
            "        numbers from time to time, such as credit cards, MoneyKit attempts to keep the `account_id` constant.\n"
            "        However, if MoneyKit can't reconcile the new account data with the old data, the `account_id` may change.\n"
        )
    )
    account_type: AccountType = pydantic.Field(
        description=(
            "See <a href=/pages/account_types>Account Types</a> for an explanation of account types.\n"
            "        <p>Note that `account_type` has an effect on how balances are reported (`credit_card` and `loan` accounts\n"
            "        report liabilities as positive values; all other types of accounts report liabilities as negative\n"
            "        values).\n"
        )
    )
    name: str = pydantic.Field(
        description=(
            "The account name, according to the institution.  Note that some institutions allow\n"
            "        the end user to nickname the account; in such cases this field may be the name assigned by the user.\n"
        )
    )
    account_mask: typing.Optional[str] = pydantic.Field(
        description=(
            "The last four characters (usually digits) of the account number.\n"
            "        Note that this mask may be non-unique between accounts.\n"
        )
    )
    balances: AccountBalances = pydantic.Field(
        description=(
            "The balance of funds for this account. Note that balances are typically cached and may lag\n"
            "        behind actual values at the institution. To update balances, please use the <a href=#operation/refresh_products>/products</a> endpoint.\n"
        )
    )
    numbers: AccountNumbers = pydantic.Field(description=("The various types of account numbers.\n"))

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        json_encoders = {dt.datetime: serialize_datetime}
