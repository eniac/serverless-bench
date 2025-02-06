import warnings
import gzip
import pickle

# Suppress specific scikit-learn warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

CLASSES = {0: "negative", 4: "positive"}

MODEL_FILE = "model.dat.gz"
with gzip.open(MODEL_FILE, "rb") as f:
    MODEL = pickle.load(f, encoding="latin1")


# pylint: disable=unused-argument
def handler(event, context=None):
    """
    Validate parameters and call the recommendation engine
    @event: API Gateway's POST body;
    @context: LambdaContext instance;
    """

    # input validation
    assert event, "AWS Lambda event parameter not provided"
    text = event.get("text")  # query text
    assert isinstance(text, str)

    # call predicting function
    return predict(text)


def predict(text):
    """
    Predict the sentiment of a string
    @text: string - the string to be analyzed
    """

    x_vector = MODEL.vectorizer.transform([text])
    y_predicted = MODEL.predict(x_vector)

    return CLASSES.get(y_predicted[0])


if __name__ == "__main__":
    print(handler({"text": "I love this movie"}))
    print(handler({"text": "I hate this movie"}))
    print(handler({"text": "I don't know what to say"}))
    print(handler({"text": "I'm not sure about this"}))
