from textblob import TextBlob
import os

os.environ["NLTK_DATA"] = "/task/var/nltk_data/"


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
        )
    }
