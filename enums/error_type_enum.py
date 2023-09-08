from enum import Enum

class ErrorTypeEnum(Enum):
    INVALID_CURRENT_PASSWORD = 'invalid_current_password'
    INVALID_NEW_PASSWORD = 'invalid_new_password'
    INVALID_NEW_PASSWORD_CONFIRMATION = 'invalid_new_password_confirmation'
