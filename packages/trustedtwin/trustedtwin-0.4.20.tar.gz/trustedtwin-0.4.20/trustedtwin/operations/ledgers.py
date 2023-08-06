"""Definition of Ledgers access methods."""
import urllib.parse
from typing import TYPE_CHECKING, Dict, Optional, List, Any

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


class LedgersOperations:
    """Interfaces for accessing Ledgers API operations"""

    def __init__(self, service: "RestService"):
        """Initialize object"""
        self._service = service
        self._http_client = self._service.http_client

    def add_twin_ledger_entry(
        self, twin: str, ledger: str = "personal", **kwargs: Any
    ) -> Dict:
        """Execute add_twin_ledger_entry API operation"""

        endpoint = "twins/{twin}/ledgers/{ledger}".format(twin=twin, ledger=ledger)
        endpoint = urllib.parse.quote(endpoint)

        body = {"entries": kwargs["entries"]}

        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(resp, "add_twin_ledger_entry", **self._service.kwargs)

    def get_twin_ledger_entry(
        self,
        twin: str,
        ledger: str = "personal",
        show_references: Optional[bool] = None,
        show_public: Optional[bool] = None,
        show_private: Optional[bool] = None,
        entries: Optional[List[str]] = None,
    ) -> Dict:
        """Execute get_twin_ledger_entry API operation"""

        endpoint = "twins/{twin}/ledgers/{ledger}".format(twin=twin, ledger=ledger)
        endpoint = urllib.parse.quote(endpoint)
        params = {
            "entries": entries,
            "show_private": show_private,
            "show_public": show_public,
            "show_references": show_references,
        }
        params = {k: v for k, v in params.items() if v is not None}

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            params=params,
        )

        return process_response(resp, "get_twin_ledger_entry", **self._service.kwargs)

    def get_twin_ledger_entry_value(
        self,
        twin: str,
        ledger: str = "personal",
        entries: Optional[List[str]] = None
    ) -> Dict:
        """Execute get_twin_ledger_entry_value API operation"""

        endpoint = "twins/{twin}/ledgers/{ledger}/value".format(twin=twin, ledger=ledger)
        endpoint = urllib.parse.quote(endpoint)
        params = {
            "entries": entries
        }
        params = {k: v for k, v in params.items() if v is not None}

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            params=params,
        )

        return process_response(resp, "get_twin_ledger_entry_value", **self._service.kwargs)

    def update_twin_ledger_entry(
        self, twin: str, ledger: str = "personal", **kwargs: Any
    ) -> Dict:
        """Execute updateTwinLedgerEntry API operation"""

        endpoint = "twins/{twin}/ledgers/{ledger}".format(twin=twin, ledger=ledger)
        endpoint = urllib.parse.quote(endpoint)

        body = {"entries": kwargs["entries"]}

        resp = self._http_client.execute_request(
            method=RESTMethod.PATCH,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(
            resp, "update_twin_ledger_entry", **self._service.kwargs
        )

    def update_twin_ledger_entry_value(
        self, twin: str, ledger: str = "personal", **kwargs: Any
    ) -> Dict:
        """Execute update_twin_ledger_entry API operation"""

        endpoint = "twins/{twin}/ledgers/{ledger}/value".format(twin=twin, ledger=ledger)
        endpoint = urllib.parse.quote(endpoint)

        body = {"entries": kwargs["entries"]}

        resp = self._http_client.execute_request(
            method=RESTMethod.PATCH,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(
            resp, "update_twin_ledger_entry_value", **self._service.kwargs
        )

    def delete_twin_ledger_entry(
        self, twin: str, ledger: str = "personal", entries: Optional[List[str]] = None
    ) -> Dict:
        """Execute delete_twin_ledger_entry API operation"""

        endpoint = "twins/{twin}/ledgers/{ledger}".format(twin=twin, ledger=ledger)
        endpoint = urllib.parse.quote(endpoint)
        params = {"entries": entries}
        params = {k: v for k, v in params.items() if v is not None}

        resp = self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            params=params,
        )

        return process_response(
            resp, "delete_twin_ledger_entry", **self._service.kwargs
        )
