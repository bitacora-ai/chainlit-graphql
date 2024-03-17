import typing

from strawberry.permission import BasePermission
from strawberry.types import Info
from chainlit_graphql.service.apikey import ApikeyService
from chainlit_graphql.repository.apikey import apikey_repo


class IsValidApiKey(BasePermission):
    message = "Api key does not exsit!"

    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        apikey_service = ApikeyService(apikey_repo)
        request = info.context["request"]
        # Access headers for authentication
        apikey = request.headers.get("x-api-key")
        if apikey:
            return apikey_service.validate_apikey(apikey)
        return False
