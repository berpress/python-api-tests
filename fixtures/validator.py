import cattr

from requests import Response

# logger = logging.getLogger("ncps")


class Validator:
    def structure(self, response: Response, type_response) -> Response:
        """
        Try to structure response
        :param response: response
        :param type_response: type response
        :return: modify response with "data" field
        """
        if type_response:
            try:
                response.data = cattr.structure(response.json(), type_response)
            except Exception as e:
                raise e
        return response


# def _get_field_structure(type_response) -> List:
#     """
#     Return fields from response type
#     """
#     fields = []
#     for field in type_response.__attrs_attrs__:
#         fields.append(field.name)
#     return fields
#
#
# def _get_field_response(response):
#     """
#     Return fields from response
#     """
#     try:
#         return list(response.json().keys())
#     except Exception:
#         return response.text
