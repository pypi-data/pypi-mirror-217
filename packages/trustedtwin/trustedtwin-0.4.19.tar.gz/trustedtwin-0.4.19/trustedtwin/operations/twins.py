"""Definition of Twins access methods."""
import urllib.parse
from typing import TYPE_CHECKING, Dict, Optional, Any, Union

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


class TwinsOperations:
    """Interfaces for accessing Twins API operations"""

    def __init__(self, service: "RestService"):
        """Initialize object"""
        self._service = service
        self._http_client = self._service.http_client

    def create(self, **kwargs: Any) -> Dict:
        """Execute create_twin API operation"""

        endpoint = "twins"
        endpoint = urllib.parse.quote(endpoint)

        body = {}
        if "description" in kwargs:
            body["description"] = kwargs["description"]

        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(resp, "create_twin", **self._service.kwargs)

    def get(self, twin: str, show_terminated: Optional[bool] = None) -> Dict:
        """Execute get_twin API operation"""

        endpoint = "twins/{twin}".format(twin=twin)
        endpoint = urllib.parse.quote(endpoint)
        params = {"show_terminated": show_terminated}
        params = {k: v for k, v in params.items() if v is not None}

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            params=params,
        )

        return process_response(resp, "get_twin", **self._service.kwargs)

    def update(self, twin: str, **kwargs: Any) -> Dict:
        """Execute update_twin API operation"""

        endpoint = "twins/{twin}".format(twin=twin)
        endpoint = urllib.parse.quote(endpoint)

        body = {}
        if "description" in kwargs:
            body["description"] = kwargs["description"]

        resp = self._http_client.execute_request(
            method=RESTMethod.PATCH,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(resp, "update_twin", **self._service.kwargs)

    def terminate(self, twin: str) -> Dict:
        """Execute terminate_twin API operation"""

        endpoint = "twins/{twin}".format(twin=twin)
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "terminate_twin", **self._service.kwargs)

    def scan(self,
             cursor: Union[None, str],
             match: Optional[str] = None,
             count: Optional[int] = None,
             details: Optional[bool] = None) -> dict:
        """Execute scan_twins API operation"""

        params = {"match": match, "count": count, "details": details, "cursor": cursor}

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint="twins",
            params=params
        )

        return process_response(resp, "scan_twins", **self._service.kwargs)
