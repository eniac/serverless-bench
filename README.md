# ServerlessBench

This repository contains a set of Python serverless applications.

## Installation

Simply clone this directory:

```console
$ git clone https://github.com/spyrospav/serverless-examples
```

## Structure

To make use of the benchmark and the tools that come with it, we highly encourage to use the following structure for your application:

1. Move to the `examples` directory and create a new directory for your application.
   
    ```console
    $ cd examples
    $ mkdir app
    ```
2. Follow the file specification by naming your main file as `lambda.py` and by putting your Lambda function handler in a function named `handler`.
  
    ```python
    def handler(event, context):
        ...
    ```

3. (Optional) Create the requirements file for your application, e.q. by using:

    ```console
    $ pip freeze > requirements.txt
    ```

4. Provide some test cases in a file called `data.json`. For more details in the structure of this file refer to section [Test cases format](#test-cases-format).

## Usage

## Test cases format

Each test case is `JSON` object with three proreties/key-value pairs:

1. `"name"` corresponding to the test case name.
2. `"event"` corresponding to the `event` argument of the lambda handler.
3. `"context"` corresponding to the `context` argument of the lambda handler.

Then, the `data.json` file contains a list of test cases under the property `"tests"`.

```json
{
    "tests": [
        {
            "name": ...,
            "event": ...,
            "context": ...
        },
        ...
    ]
}
```

