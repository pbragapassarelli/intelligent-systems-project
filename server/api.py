from flask import Flask
from flask import request
from flask import jsonify

import os
import pickle

import scipy as sp
import pandas as pd


# Loading fitted model and word vetor at application start
WORD_VECTOR_PATH = os.getenv("WORD_VECTOR_PATH")
MODEL_PATH = os.getenv("MODEL_PATH")

with open(WORD_VECTOR_PATH, 'rb') as f:
    word_vector = pickle.load(f)

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)


# Error messages
MESSAGE_FAILED_DATAFRAME = 'Failed to create a Dataframe. Check input schema.'
MESSAGE_FAILED_TO_PARSE_CONCATENATED_TAGS = 'Failed to parse concatenated_tags field. \
    It is either not a string or is absent on some products.'
MESSAGE_FAILED_MISSING_FIELDS = 'There are missing fields on all products of the input.'
MESSAGE_FAILED_TO_PREDICT = 'Could not generate predictions. \
    Check data types or missing fields on some products of the input.'


# Instanciating Flask app
app = Flask(__name__)


# Class to treat errors
class InvalidUsage(Exception):

    def __init__(self, message, status_code=400, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


# Flask error handler
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


# Flask route
@app.route("/v1/categorize", methods=["POST"])
def categorize():
    try:
        df = pd.DataFrame(request.json['products'])
    except:
        raise InvalidUsage(MESSAGE_FAILED_DATAFRAME)

    dense_columns = [
        'search_page',
        'position',
        'price',
        'weight',
        'minimum_quantity',
        'view_counts',
        'order_counts',
        'express_delivery'
    ]

    text_column = 'concatenated_tags'

    try:
        text_set = df[text_column]
        dense_set = df[dense_columns].values
    except:
        raise InvalidUsage(MESSAGE_FAILED_MISSING_FIELDS)

    try:
        text_list = [word for word in text_set]
        sparse_tags = word_vector.transform(text_list)
    except:
        raise InvalidUsage(MESSAGE_FAILED_TO_PARSE_CONCATENATED_TAGS)

    final_set = sp.sparse.hstack(
        (
            sparse_tags,
            dense_set
        ),
        format='csr'
    )

    try:
        results = model.predict(final_set)
    except:
        raise InvalidUsage(MESSAGE_FAILED_TO_PREDICT)

    return { "categories": list(results) }
