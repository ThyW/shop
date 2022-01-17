import re


def is_mail(input: str) -> bool:
    expr = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(expr, input):
        return True
    return False
