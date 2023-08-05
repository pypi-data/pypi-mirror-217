# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class TransactionType(str, enum.Enum):
    """
    An enumeration.
    """

    CREDIT = "credit"
    DEBIT = "debit"

    def visit(self, credit: typing.Callable[[], T_Result], debit: typing.Callable[[], T_Result]) -> T_Result:
        if self is TransactionType.CREDIT:
            return credit()
        if self is TransactionType.DEBIT:
            return debit()
