# coding=utf-8
"""ImageResize Lambda function handler"""
from __future__ import print_function

import time
IMPORT_START_TIME = time.time()
import boto3
from wand.image import Image
import os
IMPORT_END_TIME = time.time()
print(f"<import {IMPORT_END_TIME - IMPORT_START_TIME} seconds>")
BUCKET_NAME = "serverless-torch-xl"
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


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
        filter_name = 'mitchell'
    else:
        filter_name = 'lanczos2'

    image.resize(width=resize_width, height=resize_height, filter=filter_name, blur=1)

    return image


def handler(event, context):
    """Handle an S3 event on the target bucket to resize and save to destination bucket

    Example Event:
    {
      "Records": [
        {
          "eventVersion": "2.0",
          "eventTime": "1970-01-01T00:00:00.000Z",
          "requestParameters": {
            "sourceIPAddress": "127.0.0.1"
          },
          "s3": {
            "configurationId": "testConfigRule",
            "object": {
              "eTag": "0123456789abcdef0123456789abcdef",
              "sequencer": "0A1B2C3D4E5F678901",
              "key": "HappyFace.jpg",
              "size": 1024
            },
            "bucket": {
              "arn": "arn:aws:s3:::mybucket",
              "name": "sourcebucket",
              "ownerIdentity": {
                "principalId": "EXAMPLE"
              }
            },
            "s3SchemaVersion": "1.0"
          },
          "responseElements": {
            "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH",
            "x-amz-request-id": "EXAMPLE123456789"
          },
          "awsRegion": "us-east-1",
          "eventName": "ObjectCreated:Put",
          "userIdentity": {
            "principalId": "EXAMPLE"
          },
          "eventSource": "aws:s3"
        }
      ]
    }

    :param event: Information of the event which triggered the invocation of this function
    :type event: dict
    :param context: The invocation context
    :type context: dict
    """
    sleep_time = event.get("sleep_time", 0)

    event = {
        "key_path": "happyFace.jpg"
    }

    # Obtain the bucket name and key for the event
    bucket_name = BUCKET_NAME
    key_path = event.get('key_path', "happyFace.jpg")

    # Retrieve the S3 Object
    s3_connection = boto3.resource('s3')
    s3_object = s3_connection.Object(bucket_name, key_path)

    response = s3_object.get()

    # Perform the resize operation
    with Image(blob=response['Body'].read()) as image:
        resized_image = resize_image(image, 400, 400)
        resized_data = resized_image.make_blob()

    # And finally, upload to the resize bucket the new image
    s3_resized_object = s3_connection.Object('test-resize', key_path)
    time.sleep(sleep_time)
    print("Resized data: ", resized_data)
    # try:
    #   s3_resized_object.put(Body=resized_data)
    #   #s3_resized_object.put(ACL='authenticated-read', Body=resized_data)

    #   # Finally remove, as the bucket is public and we don't want just anyone dumping the list of our files!
    #   s3_resized_object.delete()
    # except Exception as e:
    #     print("ignoring error: {}".format(e))
    return {"import_time": IMPORT_END_TIME - IMPORT_START_TIME}
