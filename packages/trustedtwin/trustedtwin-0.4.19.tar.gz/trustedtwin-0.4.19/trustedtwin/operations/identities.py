"""Definition of Identities access methods."""
import urllib.parse
from typing import TYPE_CHECKING, Dict, Optional, Any

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


class IdentitiesOperations:
    """Interfaces for accessing Identities API operations"""

    def __init__(self, service: "RestService"):
        """Initialize object"""
        self._service = service
        self._http_client = self._service.http_client

    def create(self, twin: str, **kwargs: Any) -> Dict:
        """Execute createTwinIdentity API operation"""

        endpoint = "twins/{twin}/identities".format(twin=twin)
        endpoint = urllib.parse.quote(endpoint)

        body = {"identities": kwargs["identities"]}

        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(resp, "create_twin_identity", **self._service.kwargs)

    def get_all(
        self,
        twin: str,
        show_expired: Optional[bool] = None,
        show_valid: Optional[bool] = None,
        show_foreign: Optional[bool] = None,
        show_public: Optional[bool] = None,
        show_private: Optional[bool] = None,
        show_personal: Optional[bool] = None,
    ) -> Dict:
        """Execute getTwinIdentities API operation"""

        endpoint = "twins/{twin}/identities".format(twin=twin)
        endpoint = urllib.parse.quote(endpoint)
        params = {
            "show_expired": show_expired,
            "show_private": show_private,
            "show_foreign": show_foreign,
            "show_public": show_public,
            "show_valid": show_valid,
            "show_personal": show_personal,
        }
        params = {k: v for k, v in params.items() if v is not None}

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            params=params,
        )

        return process_response(resp, "get_twin_identities", **self._service.kwargs)

    def update(self, twin: str, identity: str, **kwargs: Any) -> Dict:
        """Execute updateTwinIdentity API operation"""

        endpoint = "twins/{twin}/identities/{identity}".format(
            twin=twin, identity=identity
        )
        endpoint = urllib.parse.quote(endpoint)

        body = {}

        if "visibility" in kwargs:
            body["visibility"] = kwargs["visibility"]
        if "validity_ts" in kwargs:
            body["validity_ts"] = kwargs["validity_ts"]

        resp = self._http_client.execute_request(
            method=RESTMethod.PATCH,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(resp, "update_twin_identity", **self._service.kwargs)

    def get(self, twin: str, identity: str) -> Dict:
        """Execute getTwinIdentity API operation"""

        endpoint = "twins/{twin}/identities/{identity}".format(
            twin=twin, identity=identity
        )
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "get_twin_identity", **self._service.kwargs)

    def delete(self, twin: str, identity: str) -> Dict:
        """Execute deleteTwinIdentity API operation"""

        endpoint = "twins/{twin}/identities/{identity}".format(
            twin=twin, identity=identity
        )
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "delete_twin_identity", **self._service.kwargs)

    def resolve(self, identity: str, context: Optional[str] = None) -> Dict:
        """Execute deleteTwinIdentity API operation"""

        endpoint = "resolve/{identity}".format(
            identity=urllib.parse.quote(identity, safe="")
        )

        params = {
            "context": context,
        }
        params = {k: v for k, v in params.items() if v is not None}

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            params=params,
        )

        return process_response(resp, "resolve_twin_identity", **self._service.kwargs)
