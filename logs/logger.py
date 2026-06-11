from datetime import datetime


def write_log(message):

    with open(
        "logs/system.log",
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            f"[{datetime.now()}] {message}\n"
        )