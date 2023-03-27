from dataclasses import dataclass, field
from typing import Dict

from requests import Session
from requests.exceptions import RequestException
from dynaconf import settings


@dataclass
class BaseApiClient:
    uri: str = field(default_factory=str)
    timeout: int = field(default_factory=int)
    headers: dict = field(default_factory=dict)
    session: Session = field(default=Session)

    def __post_init__(self):
        self.session = Session()
        self.timeout = int(settings("request_default_timeout", 30))
        self.ssl_verify = settings.as_bool("request_ssl_verify")
        if isinstance(self.headers, dict):
            self.headers = {**self._get_default_headers(), **self.headers}
        else:
            self.headers = self._get_default_headers()

    def add_custom_header(self, key: str = None, value: str = None):
        self.headers.update({key: value})

    def clear_custom_headers(self):
        self.headers = self._get_default_headers()

    def get(self, path: str = None, params: Dict = None) -> Dict[str, any]:
        return self._execute_request("GET", path, params)

    def post(
        self, path: str = None, params: Dict = None, body: str = None
    ) -> Dict[str, any]:
        return self._execute_request("POST", path, params, body)

    def put(
        self, path: str = None, params: Dict = None, body: str = None
    ) -> Dict[str, any]:
        return self._execute_request("PUT", path, params, body)

    def patch(
        self, path: str = None, params: Dict = None, body: str = None
    ) -> Dict[str, any]:
        return self._execute_request("PATCH", path, params, body)

    def delete(self, path: str = None, params: Dict = None) -> Dict[str, any]:
        return self._execute_request("DELETE", path, params)

    def _get_default_headers(self) -> Dict[str, any]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": settings("request_default_user_agent"),
        }

    def _execute_request(
        self,
        method: str = None,
        path: str = None,
        params: Dict = None,
        body: str = None,
    ) -> Dict[str, any]:
        request_url = f'{self.uri}{path if path else ""}'
        response = {"status_code": None, "body": None, "error": None}

        try:
            http_response = self.session.request(
                method=method,
                url=request_url,
                headers=self.headers,
                params=params,
                data=body,
                timeout=self.timeout,
                verify=self.ssl_verify,
            )

            response["status_code"] = http_response.status_code
            response["body"] = http_response.text if http_response.text else None
            http_response.raise_for_status()
            return response
        except RequestException as error:
            response["error"] = error
            return response
