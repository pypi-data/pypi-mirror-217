"""Definition of Indexes access methods."""
import urllib.parse
from typing import TYPE_CHECKING, Dict, Any

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


class IndexesOperations:
    """Interfaces for accessing Indexes API operations"""

    def __init__(self, service: "RestService"):
        """Initialize object"""
        self._service = service
        self._http_client = self._service.http_client

    def get_table(self, index: str) -> Dict:
        """Execute getIndexesTable API operation"""

        endpoint = "account/services/indexes/{index}".format(index=index)
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "getIndexesTable", **self._service.kwargs)

    def delete_table(self, index: str) -> Dict:
        """Execute deleteIndexesTable API operation"""

        endpoint = "account/services/indexes/{index}".format(index=index)
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "delete_indexes_table", **self._service.kwargs)

    def update_table(self, index: str, **kwargs: Any) -> Dict:
        """Execute updateIndexesTable API operation"""

        endpoint = "account/services/indexes/{index}".format(index=index)
        endpoint = urllib.parse.quote(endpoint)

        body = {}
        if "rule" in kwargs:
            body["rule"] = kwargs["rule"]
        if "properties" in kwargs:
            body["properties"] = kwargs["properties"]
        if "templates" in kwargs:
            body["templates"] = kwargs["templates"]

        resp = self._http_client.execute_request(
            method=RESTMethod.PATCH,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(resp, "update_indexes_table", **self._service.kwargs)

    def get_tables(self) -> Dict:
        """Execute getIndexesTables API operation"""

        endpoint = "account/services/indexes"
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "get_indexes_tables", **self._service.kwargs)

    def update_access(self, **kwargs: Any) -> Dict:
        """Execute updateIndexesAccess API operation"""

        endpoint = "account/services/indexes"
        endpoint = urllib.parse.quote(endpoint)

        body = {"users": kwargs["users"]}

        resp = self._http_client.execute_request(
            method=RESTMethod.PATCH,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(resp, "update_indexes_access", **self._service.kwargs)

    def create_table(self, **kwargs: Any) -> Dict:
        """Execute createIndexesTable API operation"""

        endpoint = "account/services/indexes"
        endpoint = urllib.parse.quote(endpoint)

        body = {"indexes": kwargs["indexes"]}

        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(resp, "create_indexes_table", **self._service.kwargs)

    def truncate_table(self, index: str) -> Dict:
        """Execute truncateIndexesTable API operation"""

        endpoint = "account/services/indexes/{index}/data".format(index=index)
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "truncate_indexes_table", **self._service.kwargs)
