import pytest
import socket

from pydis.client import RedisClient


@pytest.fixture
def client():
    client = RedisClient()
    client.flushall()
    yield client
    client.flushall()


def test_command_exists__non_existing_key_returns_0(client):
    assert client.exists("non_existing_key") == 0
