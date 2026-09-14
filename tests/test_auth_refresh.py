import asyncio
import os
import unittest
from types import SimpleNamespace

from fastapi import Request, Response

os.environ.setdefault("SECRET_KEY", "test-secret-key")

from Routers import Auth, Applications, Companies, Interviews
from config import API_V1_PREFIX


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
        request = Request({"type": "http", "headers": [(b"cookie", f"refresh_token={refresh_token}".encode())], "method": "POST", "query_string": b"", "path": "/api/v1/auth/refresh", "client": ("testclient", 123), "server": ("testserver", 80), "scheme": "http", "http_version": "1.1"})
        result = asyncio.run(Auth.refresh(request=request, response=response))

        self.assertIn("access_token", result)
        self.assertEqual(result["token_type"], "bearer")
        self.assertTrue(bool(response.headers.get("set-cookie")))


class ApiV1RouteTests(unittest.TestCase):
    def test_routers_use_versionable_resource_prefixes(self):
        self.assertEqual(API_V1_PREFIX, "/api/v1")
        self.assertEqual(Auth.router.prefix, "/auth")
        self.assertEqual(Applications.router.prefix, "/applications")
        self.assertEqual(Companies.router.prefix, "/companies")
        self.assertEqual(Interviews.router.prefix, "/interviews")

        auth_paths = {route.path for route in Auth.router.routes}
        self.assertIn("/auth/register", auth_paths)
        self.assertIn("/auth/login", auth_paths)
        self.assertIn("/auth/me", auth_paths)
        self.assertIn("/auth/users", auth_paths)
        self.assertIn("/auth/password", auth_paths)
        self.assertIn("/auth/refresh", auth_paths)
        self.assertNotIn("/auth/all", auth_paths)
        self.assertNotIn("/auth/reset_password", auth_paths)

        company_paths = {route.path for route in Companies.router.routes}
        self.assertIn("/companies", company_paths)
        self.assertIn("/companies/{company_id}", company_paths)
        self.assertNotIn("/companies/company/get_all", company_paths)
        self.assertNotIn("/company_deleted/", company_paths)


if __name__ == "__main__":
    unittest.main()
