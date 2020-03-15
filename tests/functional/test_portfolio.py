import pytest
import pathlib
import json

"""
This file (test_portfolio.py) contains the functional tests for the /portfolio/ endpoint.
The tested view can be found at ../application/resources/portfolio_view.
"""


def test_portfolio_post(test_client):
    """
    GIVEN a flask application
    WHEN making a POST request to the /portfolio/ endpoint without any
    :param test_client:
    :return:
    """
    with open(str(pathlib.Path(__file__).parent.parent / "test_data/functional_portfolio_post.json"), "r") as fin:
        test_data = json.load(fin)
    response = test_client.post("/portfolio/",
                                content_type="application/json",
                                json=test_data)
    print(response.status_code)
    assert 200 <= response.status_code < 300
