from pydantic import EmailStr, ValidationError


def validate_email(value: str) -> EmailStr:
    try:
        return EmailStr.validate(value)
    except ValidationError as exc:
        raise ValueError("Invalid email format") from exc


def validate_password_strength(password: str) -> None:
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")

    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    if not (has_lower and has_upper and has_digit):
        raise ValueError("Password must include upper case, lower case, and digits")
