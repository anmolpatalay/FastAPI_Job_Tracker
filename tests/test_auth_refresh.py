import asyncio
import os
import unittest
from types import SimpleNamespace

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
    def test_login_returns_refresh_token(self):
        original_verify = Auth.bcrypt_context.verify
        Auth.bcrypt_context.verify = lambda password, hashed_password: True
        try:
            result = asyncio.run(
                Auth.login(
                    db=DummyDB(DummyUser()),
                    form_data=SimpleNamespace(username="user@example.com", password="password"),
                )
            )
        finally:
            Auth.bcrypt_context.verify = original_verify

        self.assertIn("access_token", result)
        self.assertIn("refresh_token", result)
        self.assertEqual(result["token_type"], "bearer")

    def test_refresh_endpoint_returns_new_tokens(self):
        refresh_token = Auth.create_refresh_token("user@example.com", 1)
        result = asyncio.run(Auth.refresh(refresh_token))

        self.assertIn("access_token", result)
        self.assertIn("refresh_token", result)
        self.assertEqual(result["token_type"], "bearer")


if __name__ == "__main__":
    unittest.main()
