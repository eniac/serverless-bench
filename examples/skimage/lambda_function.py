import time
IMPORT_START_TIME = time.time()
from skimage import io
from skimage.segmentation import felzenszwalb
from skimage.color import label2rgb
import urllib3
IMPORT_END_TIME = time.time()

def handler(event, context=None):
    event = {
        "url": "https://upload.wikimedia.org/wikipedia/commons/3/38/JPEG_example_JPG_RIP_001.jpg",
        "filename": "test.jpg"
    }
    DIR = "/tmp/"
    url = event.get("url")
    # Create a PoolManager instance
    http = urllib3.PoolManager()
    
    # Make a GET request to the URL
    response = http.request('GET', url)

    # Save the response data to a file
    filename = event.get("filename")
    with open(DIR + filename, 'wb') as f:
        f.write(response.data)

    # Read the image
    img = io.imread(DIR + filename)
    
    # Apply felzenszwalb segmentation
    segments = felzenszwalb(img, scale=100, sigma=0.5, min_size=50)
    
    # Convert segmented image into an RGB overlay for visualization
    segmented_image = label2rgb(segments, img, kind='avg')

    io.imsave(DIR + "segmented_" + filename, segmented_image)
    
    return {"import_time": IMPORT_END_TIME - IMPORT_START_TIME}
