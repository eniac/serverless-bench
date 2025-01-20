import io
import time
import os
import sys
import json

# start = time.time()
import torch

# end = time.time()
# torch_import_time = end - start

# start = time.time()
from torchvision import transforms
from torchvision.models import resnet50

# end = time.time()
# torchvision_import_time = end - start

from PIL import Image

import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

model = None


def download(url, local_path, filename):
    if not os.path.isfile(local_path + filename):
        with open(local_path + filename, "wb") as f:
            f.write(requests.get(url).content)


def handler(event, context=None):

    image_name = event["image_name"]
    image_url = event["image_url"]
    model_name = event["model_name"]
    model_url = event["model_url"]
    dataset_name = event["dataset_name"]
    dataset_url = event["dataset_url"]
    local_path = event["local_path"]

    # Download dataset
    download(dataset_url, local_path, dataset_name)

    class_idx = json.load(open(os.path.join(local_path, dataset_name), "r"))
    idx2label = [class_idx[str(k)][1] for k in range(len(class_idx))]

    # Download image
    download(image_url, local_path, image_name)

    global model

    if not model:
        # Download model checkpoint
        download(model_url, local_path, model_name)

        model = resnet50(pretrained=False)
        model.load_state_dict(torch.load(local_path + model_name))
        model.eval()

    input_image = Image.open(local_path + image_name)
    preprocess = transforms.Compose(
        [
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(
        0
    )  # create a mini-batch as expected by the model

    output = model(input_batch)
    _, index = torch.max(output, 1)
    # The output has unnormalized scores. To get probabilities, you can run a softmax on it.
    prob = torch.nn.functional.softmax(output[0], dim=0)
    _, indices = torch.sort(output, descending=True)
    ret = idx2label[index]
    results = "Prediction: index {}, class {}".format(index.item(), ret)

    return {"result": results}


if __name__ == "__main__":
    print(lambda_handler(None))
