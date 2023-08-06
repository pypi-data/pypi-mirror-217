"""Definition of Roles access methods."""
import urllib.parse
from typing import TYPE_CHECKING, Dict, Any

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


class RolesOperations:
    """Interfaces for accessing Roles API operations"""

    def __init__(self, service: "RestService"):
        """Initialize object"""
        self._service = service
        self._http_client = self._service.http_client

    def get_all(self) -> Dict:
        """Execute getUserRoles API operation"""

        endpoint = "roles"
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "get_user_roles", **self._service.kwargs)

    def create(self, **kwargs: Any) -> Dict:
        """Execute createUserRole API operation"""

        endpoint = "roles"
        endpoint = urllib.parse.quote(endpoint)

        body = {}
        if "name" in kwargs:
            body["name"] = kwargs["name"]
        if "rules" in kwargs:
            body["rules"] = kwargs["rules"]
        if "statement" in kwargs:
            body["statement"] = kwargs["statement"]

        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(resp, "create_user_role", **self._service.kwargs)

    def get(self, role: str) -> Dict:
        """Execute getUserRole API operation"""

        endpoint = "roles/{role}".format(role=role)
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "get_user_role", **self._service.kwargs)

    def delete(self, role: str) -> Dict:
        """Execute deleteUserRole API operation"""

        endpoint = "roles/{role}".format(role=role)
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "delete_user_role", **self._service.kwargs)

    def update(self, role: str, **kwargs: Any) -> Dict:
        """Execute updateUserRole API operation"""

        endpoint = "roles/{role}".format(role=role)
        endpoint = urllib.parse.quote(endpoint)

        body = {}
        if "name" in kwargs:
            body["name"] = kwargs["name"]
        if "rules" in kwargs:
            body["rules"] = kwargs["rules"]
        if "statement" in kwargs:
            body["statement"] = kwargs["statement"]

        resp = self._http_client.execute_request(
            method=RESTMethod.PATCH,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(resp, "update_user_role", **self._service.kwargs)
