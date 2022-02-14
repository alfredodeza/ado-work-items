import pytest
import ado_automate
from ado_automate import get_token


class MockAzureError(Exception):
    pass


def raise_(exception, message=""):
    raise exception(message)


def test_default_credential_raises(monkeypatch):
    monkeypatch.setattr(ado_automate, 'DefaultAzureCredential', lambda: raise_(MockAzureError))
    with pytest.raises(MockAzureError):
        get_token()


def test_default_secret_client_raises(monkeypatch):
    monkeypatch.setattr(ado_automate, 'SecretClient', lambda **x: raise_(MockAzureError))
    with pytest.raises(MockAzureError):
        get_token()
