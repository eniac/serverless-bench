import time

IMPORT_START_TIME = time.time()
import requests
from lxml import html

import_time = time.time() - IMPORT_START_TIME
print(f"<import {import_time} seconds>")


def handler(event, context):
    sleep_time = event.get("sleep_time", 0)
    url = "https://github.com/spyrospav"
    response = requests.request("GET", url)
    tree = html.fromstring(response.content)
    # Extract the username using XPath
    username = tree.find_class("vcard-username")[0].text_content()

    # remove spaces and newlines
    username = username.strip()

    time.sleep(sleep_time)

    return {"result": str(username), "import_time": import_time}


if __name__ == "__main__":
    event = {}
    context = {}
    print(handler(event, context))
