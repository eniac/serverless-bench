import requests
from lxml import html


def handler(event, context):
    url = event["url"]
    response = requests.request("GET", url)
    tree = html.fromstring(response.content)
    # Extract the username using XPath
    username = tree.find_class("vcard-username")[0].text_content()

    # remove spaces and newlines
    username = username.strip()

    return username
