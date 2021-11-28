# flask imports
from flask import Flask, request, jsonify

# Torch imports
import torch
import torch.nn as nn
import torch.nn.functional as F

# Transformers
from transformers import AutoModel, AutoTokenizer 

# global Flask instance
app = Flask(__name__)


# Define BERT model for spam detection
num_classes = 2
dropout_rate = 0.0
text_spam_model_name = "mrm8488/bert-tiny-finetuned-sms-spam-detection"

text_spam_classifier = AutoModel.from_pretrained(text_spam_model_name)
tokenizer = AutoTokenizer.from_pretrained(text_spam_model_name)
dropout_layer = nn.Dropout(p=dropout_rate)
linear_layer = nn.Linear(text_spam_classifier.config.hidden_size, num_classes)

with torch.no_grad():
    print("Hello")
    base_sentence = "Camera - You are awarded a SiPix Digital Camera! call 09061221066 from landline. Delivery within 28 days."
    base_tokenized = tokenizer(base_sentence, return_tensors="pt")
    dummy_output = text_spam_classifier(**base_tokenized)
    base_result = linear_layer(dropout_layer(dummy_output['pooler_output']))
    base_spam = torch.argmax(F.softmax(base_result)).item()
    print("base_result: ", F.softmax(base_result, dim=-1))

@app.route("/")
def index():
    return "Hi! This is the index page of spam utils."


@app.route("/spam/check_description", methods = ['POST', 'GET'])
def check_spam_on_description():

    id = request.json["id"]
    description = request.json["description"]

    # print("base result: ", base_spam)

    with torch.no_grad():
        tokenized_description = tokenizer(description, return_tensors="pt")
        model_output = text_spam_classifier(**tokenized_description)

        # get 0 or 1 value from the classifer output
        result = linear_layer(dropout_layer(model_output['pooler_output']))
        is_spam = torch.argmax(F.softmax(result)).item()

        print("is_spam values: ", F.softmax(result, dim=-1))
        print("is_spam: ", is_spam)
        # print("base_spam: ", base_spam)
        is_spam = True if is_spam == base_spam else False

        response = {
            "id": id,
            "isSpam": is_spam
        }

        return jsonify(response)
