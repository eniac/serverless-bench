"""Refactored from the examples at https://github.com/aymericdamien/TensorFlow-Examples"""

import time
IMPORT_START_TIME = time.time()
import os
import sys
import json
import configparser


# ask AWS to pick up pre-compiled dependencies from the vendored folder ?
HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(HERE, "vendored"))

# shutup tensorflow
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


import tensorflow as tf  # noqa: E402
import numpy  # noqa: E402
IMPORT_END_TIME = time.time()
print(f"<import {IMPORT_END_TIME - IMPORT_START_TIME} seconds>")
rng = numpy.random
rng.seed(42)
tf.random.set_seed(42)


class TensorFlowRegressionModel:
    def __init__(self, config: configparser.ConfigParser, is_training=True):
        self.W = tf.Variable(rng.randn(), name="weight")
        self.b = tf.Variable(rng.randn(), name="bias")

        self.optimizer = tf.optimizers.SGD(float(config.get("model", "LEARNING_RATE")))
        self.checkpoint = tf.train.Checkpoint(W=self.W, b=self.b)

        if not is_training:
            self.restore_model(config.get("model", "LOCAL_MODEL_FOLDER"))

    def linear_regression(self, x):
        return self.W * x + self.b

    def mean_square(self, y_pred, y_true):
        return tf.reduce_mean(tf.square(y_pred - y_true))

    def restore_model(self, model_dir):
        latest_checkpoint = tf.train.latest_checkpoint(model_dir)
        if latest_checkpoint:
            self.checkpoint.restore(latest_checkpoint).assert_consumed()

    def train(
        self, train_X, train_Y, learning_rate, training_epochs, model_output_dir=""
    ):
        saver = tf.train.CheckpointManager(
            self.checkpoint, model_output_dir, max_to_keep=3
        )
        for epoch in range(training_epochs):
            with tf.GradientTape() as g:
                pred = self.linear_regression(train_X)
                loss = self.mean_square(pred, train_Y)

            # Compute gradients.
            gradients = g.gradient(loss, [self.W, self.b])

            # Update W and b following gradients.
            self.optimizer.apply_gradients(zip(gradients, [self.W, self.b]))

            saver.save()

    def predict(self, x_val):
        return float(self.linear_regression(x_val).numpy())


"""
Declare here global objects living across requests
"""
# use Pythonic ConfigParser to handle settings
Config = configparser.ConfigParser()
Config.read(HERE + "/settings.ini")
# instantiate the tf_model in "prediction mode"
tf_model = TensorFlowRegressionModel(Config, is_training=True)


def validate_input(input_val):
    """
    Helper function to check if the input is indeed a float

    :param input_val: the value to check
    :return: the floating point number if the input is of the right type, None if it cannot be converted
    """
    try:
        float_input = float(input_val)
        return float_input
    except ValueError:
        return None


def get_param_from_url(event, param_name):
    """
    Helper function to retrieve query parameters from a Lambda call. Parameters are passed through the
    event object as a dictionary.

    :param event: the event as input in the Lambda function
    :param param_name: the name of the parameter in the query string
    :return: the parameter value
    """
    params = event["queryStringParameters"]
    return params[param_name]


def return_lambda_gateway_response(code, body):
    """
    This function wraps around the endpoint responses in a uniform and Lambda-friendly way

    :param code: HTTP response code (200 for OK), must be an int
    :param body: the actual content of the response
    """
    return {"statusCode": code, "body": json.dumps(body)}


def handler(event, context):
    """
    This is the function called by AWS Lambda, passing the standard parameters "event" and "context"
    When deployed, you can try it out pointing your browser to

    {LambdaURL}/{stage}/predict?x=2.7

    where {LambdaURL} is Lambda URL as returned by serveless installation and {stage} is set in the
    serverless.yml file.

    """
    sleep_time = event.get("sleep_time", 0)
    time.sleep(sleep_time)
    event = {"queryStringParameters": {"x": 2.7}}
    try:
        param = get_param_from_url(event, "x")
        x_val = validate_input(param)
        if x_val:
            value = tf_model.predict(x_val)
        else:
            raise ValueError("Input parameter has invalid type: float expected")
    except Exception as ex:
        error_response = {"error_message": "Unexpected error", "stack_trace": str(ex)}
        return {"import_time": IMPORT_END_TIME - IMPORT_START_TIME}

    return {"import_time": IMPORT_END_TIME - IMPORT_START_TIME}


