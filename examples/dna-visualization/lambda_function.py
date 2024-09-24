import time
start = time.time()
import os
import sys
import json
import_time = time.time() - start
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from squiggle import transform

def visualize(data1, data2):
    
    return transform(data1) + transform(data2)

def handler(event, context=None):
    event = {
        "dna1": "gene1.txt",
        "dna2": "gene2.txt"
    }
    
    local_path = event.get("local_path", "./")

    # Visualize sequences
    filename1 = os.path.join(local_path, event.get("dna1"))
    data1 = open(filename1, "r").read()
    filename2 = os.path.join(local_path, event.get("dna2"))
    data2 = open(filename2, "r").read()
    
    result = visualize(data1, data2)
    print(result)

    return {
        "import_time": import_time
    }

if __name__ == "__main__":
    event = {
        "dna1": "gene1.txt",
        "dna2": "gene2.txt"
    }
    print(handler(event))