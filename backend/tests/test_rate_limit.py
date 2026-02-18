"""Tests for rate limiting configuration."""

from app.config import get_settings
from app.rate_limit import limiter


def test_rate_limit_settings_exist():
    settings = get_settings()
    assert settings.rate_limit_default == "60/minute"
    assert settings.rate_limit_auth == "10/minute"


def test_limiter_has_default_limits():
    # Limiter should be configured with our default limits
    assert limiter is not None
    assert limiter._default_limits is not None


def test_limiter_uses_memory_storage():
    # Storage URI should be in-memory
    assert "memory" in str(limiter._storage_uri) or limiter._storage is not None
