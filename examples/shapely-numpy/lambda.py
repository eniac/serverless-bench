import numpy
from shapely.geometry import Point


def handler(event, context):
    x = event["x"]
    y = event["y"]
    buf = event["buffer"]
    patch = Point(x, y).buffer(buf)
    return patch.area


if __name__ == "__main__":
    area = handler(42, 42)
    print(area)
