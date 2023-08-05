# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class AccountType(str, enum.Enum):
    """
    An enumeration.
    """

    DEPOSITORY_CASH = "depository.cash"
    DEPOSITORY_CHECKING = "depository.checking"
    DEPOSITORY_SAVINGS = "depository.savings"
    DEPOSITORY_PREPAID = "depository.prepaid"
    DEPOSITORY_OTHER = "depository.other"
    CREDIT_CARD = "credit_card"
    LOAN_GENERAL = "loan.general"
    LOAN_MORTGAGE = "loan.mortgage"
    LOAN_OTHER = "loan.other"
    INVESTMENT = "investment"
    OTHER = "other"

    def visit(
        self,
        depository_cash: typing.Callable[[], T_Result],
        depository_checking: typing.Callable[[], T_Result],
        depository_savings: typing.Callable[[], T_Result],
        depository_prepaid: typing.Callable[[], T_Result],
        depository_other: typing.Callable[[], T_Result],
        credit_card: typing.Callable[[], T_Result],
        loan_general: typing.Callable[[], T_Result],
        loan_mortgage: typing.Callable[[], T_Result],
        loan_other: typing.Callable[[], T_Result],
        investment: typing.Callable[[], T_Result],
        other: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is AccountType.DEPOSITORY_CASH:
            return depository_cash()
        if self is AccountType.DEPOSITORY_CHECKING:
            return depository_checking()
        if self is AccountType.DEPOSITORY_SAVINGS:
            return depository_savings()
        if self is AccountType.DEPOSITORY_PREPAID:
            return depository_prepaid()
        if self is AccountType.DEPOSITORY_OTHER:
            return depository_other()
        if self is AccountType.CREDIT_CARD:
            return credit_card()
        if self is AccountType.LOAN_GENERAL:
            return loan_general()
        if self is AccountType.LOAN_MORTGAGE:
            return loan_mortgage()
        if self is AccountType.LOAN_OTHER:
            return loan_other()
        if self is AccountType.INVESTMENT:
            return investment()
        if self is AccountType.OTHER:
            return other()
