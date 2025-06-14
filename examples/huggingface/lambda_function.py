import time

IMPORT_START_TIME = time.time()
import json

import torch
from transformers import AutoConfig, AutoModelForQuestionAnswering, AutoTokenizer

IMPORT_END_TIME = time.time()
print(f"<import {IMPORT_END_TIME - IMPORT_START_TIME} seconds>")
import_time = IMPORT_END_TIME - IMPORT_START_TIME


def encode(tokenizer, question, context):
    """encodes the question and context with a given tokenizer"""
    encoded = tokenizer.encode_plus(question, context)
    return encoded["input_ids"], encoded["attention_mask"]


def decode(tokenizer, token):
    """decodes the tokens to the answer with a given tokenizer"""
    answer_tokens = tokenizer.convert_ids_to_tokens(token, skip_special_tokens=True)
    return tokenizer.convert_tokens_to_string(answer_tokens)


def serverless_pipeline(model_path="./model"):
    """Initializes the model and tokenzier and returns a predict function that ca be used as pipeline"""
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForQuestionAnswering.from_pretrained(model_path)

    def predict(question, context):
        """predicts the answer on an given question and context. Uses encode and decode method from above"""
        input_ids, attention_mask = encode(tokenizer, question, context)
        result = model(
            torch.tensor([input_ids]), attention_mask=torch.tensor([attention_mask])
        )
        start_scores, end_scores = result.start_logits, result.end_logits
        ans_tokens = input_ids[
            torch.argmax(start_scores) : torch.argmax(end_scores) + 1
        ]
        answer = decode(tokenizer, ans_tokens)
        return answer

    return predict


# initializes the pipeline
question_answering_pipeline = serverless_pipeline()


def handler(event, context=None):
    sleep_time = event.get("sleep_time", 0)
    event = {
        "body": json.dumps(
            {
                "context": "We introduce a new language representation model called BERT, which stands for idirectional Encoder Representations from Transformers. Unlike recent language epresentation models (Peters et al., 2018a; Radford et al., 2018), BERT is designed to pretrain deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be finetuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial taskspecific architecture modifications. BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement).",
                "question": "What is BERTs best score on Squadv2 ?",
            }
        )
    }
    time.sleep(sleep_time)
    try:
        # loads the incoming event into a dictonary
        body = json.loads(event["body"])
        # uses the pipeline to predict the answer
        answer = question_answering_pipeline(
            question=body["question"], context=body["context"]
        )
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps({"answer": answer}),
            "import_time": IMPORT_END_TIME - IMPORT_START_TIME,
        }
    except Exception as e:
        print(repr(e))
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps({"error": repr(e)}),
            "import_time": IMPORT_END_TIME - IMPORT_START_TIME,
        }
