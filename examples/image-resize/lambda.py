# coding=utf-8
"""ImageResize Lambda function handler"""
from __future__ import print_function

import boto3
from wand.image import Image
import os

BUCKET_NAME = "serverless-torch-xl"
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]

# session = boto3.Session(
#     aws_access_key_id=AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=AWS_SECRET_ACCESS_KEY
# )


def resize_image(image, resize_width, resize_height):
    """Resize an image

    :param image:
    :type image: wand.image.Image
    :param resize_width:
    :type resize_width: int or float
    :param resize_height:
    :type resize_height: int or float
    :return:
    :rtype: wand.image.Image
    """
    if resize_width == image.width and resize_height == image.height:
        return image

    original_ratio = image.width / float(image.height)
    resize_ratio = resize_width / float(resize_height)

    # We stick to the original ratio here, regardless of what the resize ratio is
    if original_ratio > resize_ratio:
        # If width is larger, we base the resize height as a function of the ratio of the width
        resize_height = int(round(resize_width / original_ratio))
    else:
        # Otherwise, we base the width as a function of the ratio of the height
        resize_width = int(round(resize_height * original_ratio))

    if ((image.width - resize_width) + (image.height - resize_height)) < 0:
        filter_name = "mitchell"
    else:
        filter_name = "lanczos2"

    image.resize(width=resize_width, height=resize_height, filter=filter_name, blur=1)

    return image


def handle_resize(event, context):
    """
    Handle an S3 event on the target bucket to resize and save to destination bucket
    """
    # Obtain the bucket name and key for the event
    bucket_name = BUCKET_NAME
    key_path = event.get("key_path", "happyFace.jpg")

    # Retrieve the S3 Object
    s3_connection = boto3.resource("s3")
    s3_object = s3_connection.Object(bucket_name, key_path)

    response = s3_object.get()

    # Perform the resize operation
    with Image(blob=response["Body"].read()) as image:
        resized_image = resize_image(image, 400, 400)
        resized_data = resized_image.make_blob()

    # And finally, upload to the resize bucket the new image
    s3_resized_object = s3_connection.Object("test-resize", key_path)
    print("Resized data: ", resized_data)
