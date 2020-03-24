from webargs import fields, validate
from marshmallow import Schema
from marshmallow import fields as mfields
from .data_models import CATEGORY


class QueryArgs(Schema):
    fields = fields.DelimitedList(fields.Str(validate=validate.Length(min=1)))
    type = mfields.Str(required=True, validate=lambda v: v in CATEGORY)
