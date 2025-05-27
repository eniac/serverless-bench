import time

IMPORT_START_TIME = time.time()
import gzip
import pickle
import warnings

IMPORT_END_TIME = time.time()
import_time = IMPORT_END_TIME - IMPORT_START_TIME
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
    prediction = predict(text)
    return {
        "import_time": IMPORT_END_TIME - IMPORT_START_TIME,
        "prediction": prediction,
    }


def predict(text):
    """
    Predict the sentiment of a string
    @text: string - the string to be analyzed
    """

    x_vector = MODEL.vectorizer.transform([text])
    y_predicted = MODEL.predict(x_vector)

    return CLASSES.get(y_predicted[0])
