from unittest import TestCase
from json import loads

from responses import activate, add, GET, POST, PUT, PATCH, DELETE

from app.clients.base_api import BaseApiClient


class BaseApiClientTest(TestCase):
    def setUp(self):
        self.base_url = "https://postman-echo.com"
        self.default_payload = {"field_1": "value_1", "field_2": "value_2"}
        self.default_response_payload = {"response_id": 100200}
        self.custom_headers = {"Custom Header": "Value of the custom header"}
        self.default_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "fastapi-simple-starter-project",
        }
        self.api_client = BaseApiClient(uri=self.base_url, headers=None)

    @activate
    def test_when_I_call_a_get_method_then_should_be_success(self):
        path_uri = "/get"

        add(
            GET,
            f"{self.base_url}{path_uri}",
            json=self.default_response_payload,
            status=200,
        )
        get_stuff = self.api_client.get(path_uri)
        self.assertEqual(loads(get_stuff.get("body")), self.default_response_payload)
        self.assertEqual(get_stuff.get("status_code"), 200)
        self.assertIsNone(get_stuff.get("error"))

    @activate
    def test_when_I_call_a_post_method_then_should_be_success(self):
        path_uri = "/post"

        add(
            POST,
            f"{self.base_url}{path_uri}",
            json=self.default_response_payload,
            status=200,
        )
        post_stuff = self.api_client.post(path_uri, body=self.default_payload)
        self.assertEqual(loads(post_stuff.get("body")), self.default_response_payload)
        self.assertEqual(post_stuff.get("status_code"), 200)
        self.assertIsNone(post_stuff.get("error"))

    @activate
    def test_when_I_call_a_put_method_then_should_be_success(self):
        path_uri = "/put"

        add(
            PUT,
            f"{self.base_url}{path_uri}",
            json=self.default_response_payload,
            status=200,
        )
        put_stuff = self.api_client.put(path_uri, body=self.default_payload)
        self.assertEqual(loads(put_stuff.get("body")), self.default_response_payload)
        self.assertEqual(put_stuff.get("status_code"), 200)
        self.assertIsNone(put_stuff.get("error"))

    @activate
    def test_when_I_call_a_patch_method_then_should_be_success(self):
        path_uri = "/patch"

        add(
            PATCH,
            f"{self.base_url}{path_uri}",
            json=self.default_response_payload,
            status=200,
        )
        patch_stuff = self.api_client.patch(path_uri, body=self.default_payload)
        self.assertEqual(loads(patch_stuff.get("body")), self.default_response_payload)
        self.assertEqual(patch_stuff.get("status_code"), 200)
        self.assertIsNone(patch_stuff.get("error"))

    @activate
    def test_when_I_call_a_delete_method_then_should_be_success(self):
        path_uri = "/delete"

        add(DELETE, f"{self.base_url}{path_uri}", status=200)
        delete_stuff = self.api_client.delete(path_uri)
        self.assertEqual(delete_stuff.get("status_code"), 200)
        self.assertIsNone(delete_stuff.get("body"))
        self.assertIsNone(delete_stuff.get("error"))

    @activate
    def test_when_I_call_a_get_method_then_should_be_an_error(self):
        path_uri = "/get"

        add(
            GET,
            f"{self.base_url}{path_uri}",
            json=self.default_response_payload,
            status=500,
        )
        get_stuff = self.api_client.get(path_uri)
        self.assertEqual(get_stuff.get("status_code"), 500)
        self.assertIsNotNone(get_stuff.get("error"))
        self.assertIsNotNone(get_stuff.get("body"))

    def test_when_I_set_a_custom_header_then_should_be_with_all_headers(self):
        api_client_with_custom_headers = BaseApiClient(
            uri=self.base_url, headers=self.custom_headers
        )
        all_headers = self.default_headers
        all_headers.update(self.custom_headers)
        self.assertDictEqual(all_headers, api_client_with_custom_headers.headers)

    def test_when_I_call_add_custom_header_then_should_be_with_all_headers(self):
        api_client_with_custom_headers = BaseApiClient(
            uri=self.base_url, headers=self.custom_headers
        )

        custom_test_header = {"custom_test_header": "custom_test_value"}
        api_client_with_custom_headers.add_custom_header(
            "custom_test_header", "custom_test_value"
        )

        all_headers = self.default_headers
        all_headers.update(self.custom_headers)
        all_headers.update(custom_test_header)
        self.assertDictEqual(all_headers, api_client_with_custom_headers.headers)

    def test_when_I_call_clear_custom_headera_then_should_be_default_headers(self):
        api_client_with_custom_headers = BaseApiClient(
            uri=self.base_url, headers=self.custom_headers
        )
        api_client_with_custom_headers.add_custom_header(
            "custom_test_header", "custom_test_value"
        )
        api_client_with_custom_headers.clear_custom_headers()

        self.assertDictEqual(
            self.default_headers, api_client_with_custom_headers.headers
        )

    @activate
    def test_when_I_call_a_get_and_has_no_response_should_be_success(self):
        path_uri = "/get"
        dict_to_test = {"status_code": 0, "body": None, "error": None}
        add(GET, f"{self.base_url}{path_uri}", json=None, status=0)
        response = self.api_client.get(path_uri)
        self.assertDictEqual(response, dict_to_test)
