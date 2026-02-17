"""Tests for authentication & authorization.

Covers:
- Login (success, wrong password, unknown user)
- /auth/me (valid token, expired/invalid, no token)
- /auth/register (admin-only, duplicate username)
- Admin route protection (admin ok, non-admin 403, unauthenticated 401)
- Password hashing & verification
- JWT creation & decoding
"""

import pytest
from httpx import AsyncClient

from app.models.user import User
from app.services.auth_service import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)

# ---------------------------------------------------------------------------
# Unit: password hashing
# ---------------------------------------------------------------------------


class TestPasswordHashing:
    def test_hash_and_verify_match(self):
        hashed = hash_password("secret123")
        assert verify_password("secret123", hashed)

    def test_wrong_password_fails(self):
        hashed = hash_password("secret123")
        assert not verify_password("wrong", hashed)

    def test_hash_is_not_plaintext(self):
        hashed = hash_password("secret123")
        assert hashed != "secret123"


# ---------------------------------------------------------------------------
# Unit: JWT tokens
# ---------------------------------------------------------------------------


class TestJWT:
    def test_create_and_decode_token(self):
        token = create_access_token(data={"sub": "admin"})
        assert decode_access_token(token) == "admin"

    def test_invalid_token_returns_none(self):
        assert decode_access_token("invalid.token.here") is None

    def test_token_missing_sub_returns_none(self):
        token = create_access_token(data={"foo": "bar"})
        assert decode_access_token(token) is None


# ---------------------------------------------------------------------------
# Integration: POST /auth/login
# ---------------------------------------------------------------------------


class TestLogin:
    @pytest.mark.usefixtures("admin_user")
    async def test_login_success(self, auth_client: AsyncClient):
        resp = await auth_client.post(
            "/api/v1/auth/login",
            data={"username": "testadmin", "password": "adminpass123"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"

    @pytest.mark.usefixtures("admin_user")
    async def test_login_wrong_password(self, auth_client: AsyncClient):
        resp = await auth_client.post(
            "/api/v1/auth/login",
            data={"username": "testadmin", "password": "wrong"},
        )
        assert resp.status_code == 401

    async def test_login_nonexistent_user(self, auth_client: AsyncClient):
        resp = await auth_client.post(
            "/api/v1/auth/login",
            data={"username": "nobody", "password": "whatever"},
        )
        assert resp.status_code == 401


# ---------------------------------------------------------------------------
# Integration: GET /auth/me
# ---------------------------------------------------------------------------


class TestMe:
    async def test_me_returns_user(self, auth_client: AsyncClient, admin_token: str):
        resp = await auth_client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["username"] == "testadmin"
        assert body["is_admin"] is True

    async def test_me_no_token(self, auth_client: AsyncClient):
        resp = await auth_client.get("/api/v1/auth/me")
        assert resp.status_code == 401

    async def test_me_invalid_token(self, auth_client: AsyncClient):
        resp = await auth_client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer bad.token.value"},
        )
        assert resp.status_code == 401


# ---------------------------------------------------------------------------
# Integration: POST /auth/register (admin-only)
# ---------------------------------------------------------------------------


class TestRegister:
    async def test_register_as_admin(self, auth_client: AsyncClient, admin_token: str):
        resp = await auth_client.post(
            "/api/v1/auth/register",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"username": "newuser", "password": "newpass123"},
        )
        assert resp.status_code == 201
        body = resp.json()
        assert body["username"] == "newuser"
        assert body["is_admin"] is False

    async def test_register_non_admin_forbidden(self, auth_client: AsyncClient, user_token: str):
        resp = await auth_client.post(
            "/api/v1/auth/register",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"username": "another", "password": "pass123456"},
        )
        assert resp.status_code == 403

    async def test_register_unauthenticated(self, auth_client: AsyncClient):
        resp = await auth_client.post(
            "/api/v1/auth/register",
            json={"username": "another", "password": "pass123456"},
        )
        assert resp.status_code == 401

    async def test_register_duplicate_username(self, auth_client: AsyncClient, admin_token: str, admin_user: User):
        resp = await auth_client.post(
            "/api/v1/auth/register",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"username": admin_user.username, "password": "pass123456"},
        )
        assert resp.status_code == 409


# ---------------------------------------------------------------------------
# Integration: Admin route protection
# ---------------------------------------------------------------------------


class TestAdminProtection:
    async def test_admin_endpoint_no_token_401(self, auth_client: AsyncClient):
        resp = await auth_client.get("/api/v1/admin/scrape/logs")
        assert resp.status_code == 401

    async def test_admin_endpoint_non_admin_403(self, auth_client: AsyncClient, user_token: str):
        resp = await auth_client.get(
            "/api/v1/admin/scrape/logs",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert resp.status_code == 403

    async def test_admin_endpoint_admin_ok(self, auth_client: AsyncClient, admin_token: str):
        resp = await auth_client.get(
            "/api/v1/admin/scrape/logs",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 200
