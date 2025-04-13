from rest_framework.exceptions import APIException


class ConflictException(APIException):
    status_code = 409
    default_detail = "Name conflict"
    default_code = "conflict"
