from api import app
from flask import json

from api import MESSAGE_FAILED_DATAFRAME, \
    MESSAGE_FAILED_MISSING_FIELDS, \
        MESSAGE_FAILED_TO_PARSE_CONCATENATED_TAGS, \
            MESSAGE_FAILED_TO_PREDICT

import pytest
import numpy as np


# Creating the payload for some products
correct_product_1 = {
    "search_page": 2,
    "position": 4,
    "price": 23.45,
    "weight": 50.3,
    "minimum_quantity": 4,
    "view_counts": 23,
    "order_counts": 12,
    "express_delivery": 0,
    "concatenated_tags": "teste tags"
}

correct_product_2 = {
    "search_page": 12,
    "position": 1,
    "price": 543.534,
    "weight": 423450.00,
    "minimum_quantity": 120,
    "view_counts": 4893,
    "order_counts": 500,
    "express_delivery": 1,
    "concatenated_tags": "TESTE tagsd"
}

missing_field_product = {
    "search_page": 12,
    "position": 1,
    "price": 543.534,
    "concatenated_tags": "TESTE tagsd"
}

none_order_counts_product = {
    "search_page": 12,
    "position": 1,
    "price": 543.534,
    "weight": 423450.00,
    "minimum_quantity": 120,
    "view_counts": 4893,
    "order_counts": np.nan,
    "express_delivery": 1,
    "concatenated_tags": "TESTE tagsd"
}

unparseable_tags_product = {
    "search_page": 12,
    "position": 1,
    "price": 543.534,
    "weight": 423450.00,
    "minimum_quantity": 120,
    "view_counts": 4893,
    "order_counts": "a",
    "express_delivery": 1,
    "concatenated_tags": 45
}

# Creating some inputs for the tests
correct_input1 = {
    "products": [
        correct_product_1,
        correct_product_2
    ]
}

correct_input2 = {
    "products": [
        correct_product_1
    ]
}

invalid_schema_input = [
    correct_product_1,
    correct_product_2
]

one_product_missing_fields_input = {
    "products": [
        correct_product_1,
        missing_field_product
    ]
}

only_missing_fields_input = {
    "products": [
        missing_field_product
    ]
}

none_order_counts_input = {
    "products": [
        none_order_counts_product
    ]
}

unparseable_tags_input = {
    "products": [
        unparseable_tags_product
    ]
}


# Declaring the tuples with (input, expected result)
list_of_expectations_status_code = [
    (correct_input1, 200),
    (correct_input2, 200),
    (invalid_schema_input, 400),
    (one_product_missing_fields_input, 400),
    (only_missing_fields_input, 400),
    (none_order_counts_input, 400),
    (unparseable_tags_input, 400)
]

list_of_expectations_messages = [
    (invalid_schema_input, MESSAGE_FAILED_DATAFRAME),
    (one_product_missing_fields_input, MESSAGE_FAILED_TO_PREDICT),
    (only_missing_fields_input, MESSAGE_FAILED_MISSING_FIELDS),
    (none_order_counts_input, MESSAGE_FAILED_TO_PREDICT),
    (unparseable_tags_input, MESSAGE_FAILED_TO_PARSE_CONCATENATED_TAGS)
]


# Making the tests
@pytest.mark.parametrize("test_input, expected", list_of_expectations_status_code)
def test_no_products_status_code(test_input, expected):
    response = app.test_client().post(
        "/v1/categorize",
        data=json.dumps(test_input),
        content_type="application/json"
    )
    assert response.status_code == expected

@pytest.mark.parametrize("test_input, expected", list_of_expectations_messages)
def test_no_products_message(test_input, expected):
    response = app.test_client().post(
        "/v1/categorize",
        data=json.dumps(test_input),
        content_type="application/json"
    )
    assert response.json['message'] == expected

