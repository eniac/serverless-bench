import time

IMPORT_START_TIME = time.time()
import json
import sys

import joblib

model_name = "model.joblib"
model = joblib.load(model_name)

import_time = time.time() - IMPORT_START_TIME
print(f"<import {import_time} seconds>")


def handler(event, context):
    sleep_time = event.get("sleep_time", 0)
    body = {
        "message": "OK",
    }
    event = {
        "queryStringParameters": {
            "medInc": 200000,
            "houseAge": 10,
            "aveRooms": 4,
            "aveBedrms": 1,
            "population": 800,
            "aveOccup": 3,
            "latitude": 37.54,
            "longitude": -121.72,
        }
    }

    if "queryStringParameters" in event.keys():
        params = event["queryStringParameters"]

        medInc = float(params["medInc"]) / 100000
        houseAge = float(params["houseAge"])
        aveRooms = float(params["aveRooms"])
        aveBedrms = float(params["aveBedrms"])
        population = float(params["population"])
        aveOccup = float(params["aveOccup"])
        latitude = float(params["latitude"])
        longitude = float(params["longitude"])

        inputVector = [
            medInc,
            houseAge,
            aveRooms,
            aveBedrms,
            population,
            aveOccup,
            latitude,
            longitude,
        ]
        data = [inputVector]
        predictedPrice = model.predict(data)[0] * 100000  # convert to units of 1 USDs
        predictedPrice = round(predictedPrice, 2)
        body["predictedPrice"] = predictedPrice

    else:
        body["message"] = "queryStringParameters not in event."

    print(body["message"])

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "import_time": import_time,
    }
    time.sleep(sleep_time)

    return response
