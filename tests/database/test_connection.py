from os import environ
from unittest import TestCase, mock

from app.database.connection import get_connection_string


@mock.patch.dict(environ, {"DATABASE_USER": "user"})
@mock.patch.dict(environ, {"DATABASE_PASSWORD": "pass"})
@mock.patch.dict(environ, {"DATABASE_URL": "host"})
@mock.patch.dict(environ, {"DATABASE_PORT": "123"})
@mock.patch.dict(environ, {"DATABASE_NAME": "name"})
class ConnectionTest(TestCase):
    def setUp(self):
        self.conn_str = "postgresql+psycopg2://user:pass@host:123/name"

    def test_when_I_call_get_connection_string_should_be_success(self):
        self.assertEqual(get_connection_string(), self.conn_str)
