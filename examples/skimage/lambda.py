# -*- coding: utf-8 -*-
from skimage import io
from skimage.segmentation import felzenszwalb
from skimage.color import label2rgb
import urllib3

def handler(event, context=None):
    url = event.get("url")
    # Create a PoolManager instance
    http = urllib3.PoolManager()
    
    # Make a GET request to the URL
    response = http.request('GET', url)

    # Save the response data to a file
    filename = event.get("filename")
    with open(filename, 'wb') as f:
        f.write(response.data)

    # Read the image
    img = io.imread(filename)
    
    # Apply felzenszwalb segmentation
    segments = felzenszwalb(img, scale=100, sigma=0.5, min_size=50)
    
    # Convert segmented image into an RGB overlay for visualization
    segmented_image = label2rgb(segments, img, kind='avg')

    io.imsave("segmented_" + filename, segmented_image)
    
    return segmented_image

if __name__ == "__main__":
    event = {
        "url": "https://upload.wikimedia.org/wikipedia/commons/3/38/JPEG_example_JPG_RIP_001.jpg",
        "filename": "test.jpg"
    }
    print(handler(event))