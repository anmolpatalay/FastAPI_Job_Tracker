import asyncio
import os
import unittest
from types import SimpleNamespace

from fastapi import Request, Response

os.environ.setdefault("SECRET_KEY", "test-secret-key")

from Routers import Auth


class DummyUser:
    def __init__(self):
        self.id = 1
        self.email = "user@example.com"
        self.hashed_password = "hashed"


class DummyQuery:
    def __init__(self, user):
        self.user = user

    def filter(self, *args, **kwargs):
        return self

    def first(self):
        return self.user


class DummyDB:
    def __init__(self, user):
        self.user = user

    def query(self, model):
        return DummyQuery(self.user)


class AuthRefreshTests(unittest.TestCase):
    def test_login_sets_refresh_cookie(self):
        original_verify = Auth.bcrypt_context.verify
        Auth.bcrypt_context.verify = lambda password, hashed_password: True
        response = Response()
        try:
            result = asyncio.run(
                Auth.login(
                    db=DummyDB(DummyUser()),
                    form_data=SimpleNamespace(username="user@example.com", password="password"),
                    response=response,
                )
            )
        finally:
            Auth.bcrypt_context.verify = original_verify

        self.assertIn("access_token", result)
        self.assertEqual(result["token_type"], "bearer")
        self.assertNotIn("refresh_token", result)
        self.assertTrue(bool(response.headers.get("set-cookie")))

    def test_refresh_endpoint_returns_new_access_token(self):
        refresh_token = Auth.create_refresh_token("user@example.com", 1)
        response = Response()
        request = Request({"type": "http", "headers": [(b"cookie", f"refresh_token={refresh_token}".encode())], "method": "POST", "query_string": b"", "path": "/Auth/refresh", "client": ("testclient", 123), "server": ("testserver", 80), "scheme": "http", "http_version": "1.1"})
        result = asyncio.run(Auth.refresh(request=request, response=response))

        self.assertIn("access_token", result)
        self.assertEqual(result["token_type"], "bearer")
        self.assertTrue(bool(response.headers.get("set-cookie")))


if __name__ == "__main__":
    unittest.main()
