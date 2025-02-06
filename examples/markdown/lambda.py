import markdown
import base64


def render(text):
    decoded_text = base64.b64decode(text.encode()).decode()
    return markdown.markdown(decoded_text)


def handler(event, context=None):
    base64_text = event["text"]
    html = render(base64_text)

    return {"result": html}


if __name__ == "__main__":
    event = {}
    print(handler(event))
