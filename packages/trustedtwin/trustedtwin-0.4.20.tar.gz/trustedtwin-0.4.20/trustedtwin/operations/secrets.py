"""Definition of Secrets access methods."""
import urllib.parse
from typing import TYPE_CHECKING, Dict, Any

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


class SecretsOperations:
    """Interfaces for accessing Secrets API operations"""

    def __init__(self, service: "RestService"):
        """Initialize object"""
        self._service = service
        self._http_client = self._service.http_client

    def get(self, user: str) -> Dict:
        """Execute getUserSecret API operation"""

        endpoint = "users/{user}/secrets".format(user=user)
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "get_user_secret", **self._service.kwargs)

    def update_secret(self, user: str, **kwargs: Any) -> Dict:
        """Execute updateUserSecret API operation"""

        endpoint = "users/{user}/secrets".format(user=user)
        endpoint = urllib.parse.quote(endpoint)

        body = {}
        if "validity_ts" in kwargs:
            body["validity_ts"] = kwargs["validity_ts"]

        resp = self._http_client.execute_request(
            method=RESTMethod.PATCH,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(resp, "update_user_secret", **self._service.kwargs)

    def delete(self, user: str) -> Dict:
        """Execute deleteUserSecret API operation"""

        endpoint = "users/{user}/secrets".format(user=user)
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "delete_user_secret", **self._service.kwargs)

    def create_secret(self, account: str, pin: str) -> Dict:
        """Execute createUserSecret API operation"""

        endpoint = "secrets/{account}/{pin}".format(account=account, pin=pin)
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "create_user_secret", **self._service.kwargs)

    def create_secret_pin(self, user: str, **kwargs: Any) -> Dict:
        """Execute createUserSecretPIN API operation"""

        endpoint = "users/{user}/secrets".format(user=user)
        endpoint = urllib.parse.quote(endpoint)

        body = {}
        if "validity_ts" in kwargs:
            body["validity_ts"] = kwargs["validity_ts"]

        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(resp, "create_user_secret_pin", **self._service.kwargs)
