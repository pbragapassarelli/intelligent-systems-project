from flask import Flask
from flask import request

import os
import pickle

import scipy as sp
import pandas as pd


WORD_VECTOR_PATH = os.getenv("WORD_VECTOR_PATH")
MODEL_PATH = os.getenv("MODEL_PATH")


with open(WORD_VECTOR_PATH, 'rb') as f:
    word_vector = pickle.load(f)

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)


app = Flask(__name__)

@app.route("/v1/categorize", methods=["POST"])
def hello_world():
    df = pd.DataFrame(request.json['products'])

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

    text_list = [word for word in df[text_column]]

    sparse_tags = word_vector.transform(text_list)

    final_set = sp.sparse.hstack(
        (
            sparse_tags,
            df[dense_columns].values
        ),
        format='csr'
    )

    results = model.predict(final_set)

    return { "categories": list(results) }