from ..extensions import api
from flask_praetorian import PraetorianError


@api.errorhandler(PraetorianError)
def handle_auth_error(error):
    return {"error": "ERR_NOT_AUTHORIZED",
            "message": "Administrative privileges are required to use this endpoint."}, 401


class AmbiguousTypeError(Exception):
    pass


@api.errorhandler(AmbiguousTypeError)
def handle_ambiguous_type(error):
    return {'error': 'ERR_AMBIGUOUS_TYPE',
            'message': 'Either a type value was not provided in the query string,'
                       ' or the type value is not "video" or "image".'}, 400


class AmbiguousFieldError(Exception):
    pass


@api.errorhandler(AmbiguousFieldError)
def handle_ambiguous_fields(error):
    return {'error': 'ERR_AMBIGUOUS_FIELDS',
            'message': 'One or some of the specified fields are not fields contained in the schema.'}, 400


class DataIntegrityError(Exception):
    pass


class DataEncodingError(Exception):
    pass


class DataRangeError(Exception):
    pass


class InvalidPurchaseItem(Exception):
    pass


@api.errorhandler(InvalidPurchaseItem)
def handle_ambiguous_type(error):
    return {'error': 'ERR_INVALID_PURCHASE_ITEM',
            'message': 'The provided item id does not correspond with a valid product.'}, 400
