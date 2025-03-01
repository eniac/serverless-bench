import time
IMPORT_START_TIME = time.time()
import json
import spacy
nlp = spacy.load("en_core_web_sm")
IMPORT_END_TIME = time.time()

def handler(event, context):
    sleep_time = event.get("sleep_time", 0)
    time.sleep(sleep_time)
    event = {
        "body": "black cat"
    }
    text = event["body"]
    doc = nlp(text)
    nouns = [token.lemma_ for token in doc if  token.pos_ == 'NOUN']

    response = {
        "statusCode": 200,
        "body": json.dumps(nouns),
        "import_time": IMPORT_END_TIME - IMPORT_START_TIME
    }

    return response

if __name__ == "__main__":
    event = {
        "body": "black cat"
    }
    print(handler(event, None))