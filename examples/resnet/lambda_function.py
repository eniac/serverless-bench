import time
IMPORT_START_TIME = time.time()
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
IMPORT_END_TIME = time.time()
print(f"<import {IMPORT_END_TIME - IMPORT_START_TIME} seconds>")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

image_name = "tesla.jpg"
image_url = "https://github.com/spcl/serverless-benchmarks-data/blob/6a17a460f289e166abb47ea6298fb939e80e8beb/400.inference/411.image-recognition/fake-resnet/800px-20180630_Tesla_Model_S_70D_2015_midnight_blue_left_front.jpg?raw=true"
model_name = "resnet50.pth"
model_url = "https://github.com/spcl/serverless-benchmarks-data/blob/6a17a460f289e166abb47ea6298fb939e80e8beb/400.inference/411.image-recognition/model/resnet50-19c8e357.pth?raw=true"
dataset_name = "imagenet_class_index.json"
dataset_url = "https://github.com/spcl/serverless-benchmarks/blob/master/benchmarks/400.inference/411.image-recognition/python/imagenet_class_index.json?raw=true"
local_path = "/tmp/"

model = None


def download(url, local_path, filename):
    if not os.path.isfile(local_path + filename):
        with open(local_path + filename, "wb") as f:
            f.write(requests.get(url).content)

def handler(event, context=None):
    sleep_time = event.get("sleep_time", 0)
    # exec_time_start = time.time()
    # Download dataset
    # start = time.time()
    download(dataset_url, local_path, dataset_name)
    # end = time.time()
    # image_download_time = end - start

    class_idx = json.load(open(os.path.join(local_path, dataset_name), 'r'))
    idx2label = [class_idx[str(k)][1] for k in range(len(class_idx))]
    
    # Download image
    download(image_url, local_path, image_name)

    global model
    # model_download_time = 0
    if not model:
        # Download model checkpoint
        # start = time.time()
        download(model_url, local_path, model_name)
        # end = time.time()
        # model_download_time = end - start

        model = resnet50(pretrained=False)
        model.load_state_dict(torch.load(local_path + model_name))
        model.eval()
   
    input_image = Image.open(local_path + image_name)
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model 

    # start = time.time()
    output = model(input_batch)
    _, index = torch.max(output, 1)
    # The output has unnormalized scores. To get probabilities, you can run a softmax on it.
    prob = torch.nn.functional.softmax(output[0], dim=0)
    _, indices = torch.sort(output, descending=True)
    ret = idx2label[index]
    results = "Prediction: index {}, class {}".format(index.item(), ret)
    # end = time.time()
    # classification_time = end - start

    # exec_time_end = time.time()
    time.sleep(sleep_time)
    return {
        "result": results,
        "import_time": IMPORT_END_TIME - IMPORT_START_TIME
        # 'torch_import_time': torch_import_time,
        # 'torchvision_import_time': torchvision_import_time,
        # 'model_download_time': model_download_time,
        # 'image_download_time': image_download_time,
        # 'classification_time': classification_time,
        # 'execution_time': exec_time_end - exec_time_start
    }

