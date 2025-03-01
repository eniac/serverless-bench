import time
IMPORT_START_TIME = time.time()
import lightgbm as lgb
import numpy
IMPORT_END_TIME = time.time()
print(f"<import {IMPORT_END_TIME - IMPORT_START_TIME} seconds>")
def handler(event, context=None):
    sleep_time = event.get("sleep_time", 0)
    event = {
        "dataset_name": "pima-indians-diabetes.csv",
        "model": "model.txt"
    }
    dataset_name = event.get("dataset_name")
    dataset = numpy.loadtxt(dataset_name, delimiter=",")
    X = dataset[:, 0:8]
    Y = dataset[:, 8]

    model = event.get("model")
    bst = lgb.Booster(model_file=model)
    Ypred = bst.predict(X)

    time.sleep(sleep_time)
    
    return {"result": numpy.mean((Ypred>0.5)==(Y==1)),
            "import_time": IMPORT_END_TIME - IMPORT_START_TIME}

if __name__ == "__main__":
    event = {
        "dataset_name": "pima-indians-diabetes.csv",
        "model": "model.txt"
    }
    print(handler(event))