"""These functions prevent the program from crashing, when a movie has N/A entries instead
of the data we expected."""


def safe_str(value):
    return value if value != "N/A" else "No info available"

def safe_float(value):
    try:
        return float(value) if value != "N/A" else None
    except ValueError:
        return None

def safe_int(value):
    try:
        return int(value) if str(value).isdigit() else None
    except (ValueError, TypeError):
        return None
