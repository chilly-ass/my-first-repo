import re
from email_validator import validate_email, EmailNotValidError


def validate_email_address(email: str) -> tuple[bool, str]:
    try:
        validated = validate_email(email, check_deliverability=False)
        return True, validated.normalized
    except EmailNotValidError as e:
        return False, str(e)


def validate_name(name: str) -> tuple[bool, str]:
    name = name.strip()
    if len(name) < 2:
        return False, "Имя слишком короткое (минимум 2 символа)"
    if len(name) > 100:
        return False, "Имя слишком длинное (максимум 100 символов)"
    return True, name
