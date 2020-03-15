import pytest
from application.resources.portfolio_image.schema import PostArgs
from marshmallow import ValidationError, pprint

"""
This file (test_portfolio_image.py) contains the unit tests for the portfolio_image resource.
The tested resource can be found at ../application/resources/portfolio_image/.
"""


def test_portfolio_image_schema():
    """
    GIVEN a PostArgs Schema
    WHEN the Schema deserializes data
    THEN check that all fields are properly validated and data is deserialized as expected
    """
    schema = PostArgs()
    data = {
        "title": "Generic Event 2020",
        "category": "portrait",
        "preview": {"uri": "data:image/jpeg;base64,iusertiusnritnseirtniudenrzidtnznerditznirdtnz", "alt": "Img Alt"},
        "content": [
            {
                "uri": "data:image/jpeg;base64,iusertiusnritnseirtniudenrzidtnznerditznirdtnz",
                "alt": "Interesting Preview"
            }
        ],
        "year": 2020,
        "client": "Pre Malone",
        "description": "Some random event info could be written here."
    }
    try:
        pprint(schema.load(data))
    except ValidationError as err:
        pytest.fail(err.messages)
