from .common import AppException


class AccountError(AppException):
    """error codes of account processing logic"""


class AccountAlreadyExist(AccountError):
    """Account with this email or phone exists"""


class NotEnoughPrivileges(AccountError):
    """The account doesn't have enough privileges"""
    status_code = 401


class InactiveAccount(AccountError):
    """Inactive account"""