import time

IMPORT_START_TIME = time.time()
import numpy
from shapely.geometry import Point


def handler(event, context):
    sleep_time = event.get("sleep_time", 0)
    time.sleep(sleep_time)
    patch = Point(0.0, 0.0).buffer(10.0)
    print(patch.area)
    return {"import_time": import_time}


if __name__ == "__main__":
    area = handler({}, {})
    print(area)

import_time = time.time() - IMPORT_START_TIME
print(f"<import {import_time} seconds>")
