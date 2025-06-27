# src/utils/validate.py
import re

def validate_name(name: str) -> bool:
    """Перевіряє, чи ПІБ не порожнє і містить лише літери, пробіли, дефіси."""
    return bool(name and re.match(r'^[\p{L}\s-]+$', name, re.UNICODE))

def validate_age(age: str) -> bool:
    """Перевіряє, чи вік — число від 16 до 100."""
    try:
        age_num = int(age)
        return 0 <= age_num <= 100
    except ValueError:
        return False

def validate_city(city: str) -> bool:
    """Перевіряє, чи місто/область не порожнє."""
    return bool(city and len(city.strip()) > 0)