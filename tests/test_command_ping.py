import pytest

from pydis.client import RedisClient


@pytest.fixture
def client():
    return RedisClient()


def test_command_ping_returns_pong(client):
    assert client.ping() == "+PONG"


def test_command_ping_with_arguments_returns_pong(client):
    assert client.ping("ARGUMENTS") == "ARGUMENTS"
