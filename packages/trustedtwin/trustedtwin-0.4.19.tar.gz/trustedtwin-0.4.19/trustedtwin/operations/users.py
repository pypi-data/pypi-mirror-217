"""Definition of Users access methods."""
import urllib.parse
from typing import TYPE_CHECKING, Dict, Any

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


class UsersOperations:
    """Interfaces for accessing Users API operations"""

    def __init__(self, service: "RestService"):
        """Initialize object"""
        self._service = service
        self._http_client = self._service.http_client

    def create(self, **kwargs: Any) -> Dict:
        """Execute create_user API operation"""

        endpoint = "users"
        endpoint = urllib.parse.quote(endpoint)

        body = {}
        if "name" in kwargs:
            body["name"] = kwargs["name"]
        if "role" in kwargs:
            body["role"] = kwargs["role"]
        if "description" in kwargs:
            body["description"] = kwargs["description"]
        if "activity" in kwargs:
            body["activity"] = kwargs["activity"]

        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(resp, "create_user", **self._service.kwargs)

    def get(self, user: str) -> Dict:
        """Execute get_user API operation"""

        endpoint = "users/{user}".format(user=user)
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "get_user", **self._service.kwargs)

    def get_all(self) -> Dict:
        """Execute get_users API operation"""

        endpoint = "users"
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "get_user", **self._service.kwargs)

    def delete(self, user: str) -> Dict:
        """Execute delete_user API operation"""

        endpoint = "users/{user}".format(user=user)
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "delete_user", **self._service.kwargs)

    def update(self, user: str, **kwargs: Any) -> Dict:
        """Execute update_user API operation"""

        endpoint = "users/{user}".format(user=user)
        endpoint = urllib.parse.quote(endpoint)

        body = {}
        if "name" in kwargs:
            body["name"] = kwargs["name"]
        if "role" in kwargs:
            body["role"] = kwargs["role"]
        if "description" in kwargs:
            body["description"] = kwargs["description"]
        if "activity" in kwargs:
            body["activity"] = kwargs["activity"]

        resp = self._http_client.execute_request(
            method=RESTMethod.PATCH,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(resp, "update_user", **self._service.kwargs)
