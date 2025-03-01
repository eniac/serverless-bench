import time
start = time.time()
import os
import snappy  # Ensure you have installed the python-snappy package: pip install python-snappy
import shutil
import uuid
import_time = time.time() - start


def compress_snappy(path, key):
    archive = os.path.join(path, '{}.snappy'.format(key))
    with open(archive, 'wb') as compressed_file:
        for root, _, files in os.walk(path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                    compressed_data = snappy.compress(file_data)
                    compressed_file.write(compressed_data)

    archive_size = os.path.getsize(archive)
    return archive, archive_size


def handler(event, context=None):
    sleep_time = event.get("sleep_time", 0)
    event = {
        'local_path': "/tmp/",
        'folder_name': "acmart"
    }
    local_path = event.get('local_path')
    folder_name = event.get('folder_name')
    archive_name, archive_size = compress_snappy(local_path, folder_name)

    time.sleep(sleep_time)
    return {
        "result": "{} compression in size {} finished!".format(archive_name, archive_size),
        "import_time": import_time
    }


if __name__ == "__main__":
    event = {
        'local_path': "./",
        'folder_name': "acmart"
    }
    print(handler(event))