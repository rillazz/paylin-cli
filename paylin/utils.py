from datetime import datetime
from slugify import slugify


def collapse_spaces(string: str):
    return " ".join(string.split())


def construct_filename(query: str, filtered: bool):
    return f"paylin_export_{slugify(query)}_{datetime.now().strftime("%Y%m%d%H%M%S")}{"_filtered" if filtered else ""}.csv"
