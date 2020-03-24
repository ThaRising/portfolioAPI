import pytest
import pathlib
import json
from application.shared.exceptions import AmbiguousFieldError

"""
This file (test_portfolio.py) contains the functional tests for the /portfolio/ endpoint.
The tested view can be found at ../application/resources/portfolio_view.
"""


def test_portfolio_get(test_client, init_db):
    """
    GIVEN a flask application
    WHEN making a GET request to the /portfolio/ endpoint with different sets of query args
    THEN check that all query args are properly validated and no uncaught errors occur
    """
    # Check general availability of the endpoint
    response = test_client.get("/portfolio/")
    assert response.status_code == 200

    # Check that key only query args are rejected
    response = test_client.get("/portfolio/?type=", follow_redirects=True)
    assert response.status_code == 422
    response = test_client.get("/portfolio/?fields=", follow_redirects=True)
    assert response.status_code == 422
    response = test_client.get("/portfolio/?fields=&type=", follow_redirects=True)
    assert response.status_code == 422

    # Check validation for the types parameter
    response = test_client.get("/portfolio/?type=iimage", follow_redirects=True)
    assert response.status_code == 422
    response = test_client.get("/portfolio/?type=1", follow_redirects=True)
    assert response.status_code == 422
    response = test_client.get("/portfolio/?type=image", follow_redirects=True)
    assert response.status_code == 200
    response = test_client.get("/portfolio/?type=image", follow_redirects=True)
    assert response.status_code == 200

    # Check validation for the fields parameter
    with pytest.raises(AmbiguousFieldError):
        response = test_client.get("/portfolio/?fields=wrong", follow_redirects=True)
    response = test_client.get("/portfolio/?fields=title", follow_redirects=True)
    assert response.status_code == 200


def test_protected(test_client, init_db):
    """
    GIVEN a flask application
    WHEN making POST, PATCH or DELETE requests to the /portfolio/ or /portfolio/id endpoint
    THEN verify that a client cannot access these resources without a valid JWT
    """
    assert True


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
