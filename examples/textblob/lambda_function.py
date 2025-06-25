import time

IMPORT_START_TIME = time.time()
import os

from textblob import TextBlob
import nltk

import_time = time.time() - IMPORT_START_TIME

os.environ["NLTK_DATA"] = "/tmp/nltk_data/"
nltk.data.path.append("/tmp/nltk_data/")


def analyze(text):
    analyse = TextBlob(text)
    num_sentences = len(analyse.sentences)
    subjectivity = (
        sum([sentence.sentiment.subjectivity for sentence in analyse.sentences])
        / num_sentences
    )
    polarity = (
        sum([sentence.sentiment.polarity for sentence in analyse.sentences])
        / num_sentences
    )
    return subjectivity, polarity


def handler(event, context=None):
    sentiment_text = event.get("text")
    subjectivity, polarity = analyze(sentiment_text)

    return {
        "result": "Sentiment analysis finished! Subjectivity {}, Polarity {}.".format(
            subjectivity, polarity
        ),
        "import_time": import_time,
    }
