from enum import Enum


class RegistrationState(str, Enum):
    CHOOSING_EVENT = "choosing_event"
    ENTERING_NAME = "entering_name"
    ENTERING_EMAIL = "entering_email"
    CONFIRMING = "confirming"
