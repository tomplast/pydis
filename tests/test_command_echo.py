import pytest
import socket

from pydis.client import RedisClient


@pytest.fixture
def client():
    return RedisClient()


def test_command_echo_returns_string(client):
    assert client.echo("Hello World") == "Hello World"
