import lightgbm as lgb
import numpy


def handler(event, context=None):
    dataset_name = event.get("dataset_name")
    dataset = numpy.loadtxt(dataset_name, delimiter=",")
    X = dataset[:, 0:8]
    Y = dataset[:, 8]

    model = event.get("model")
    bst = lgb.Booster(model_file=model)
    Ypred = bst.predict(X)

    return numpy.mean((Ypred > 0.5) == (Y == 1))
