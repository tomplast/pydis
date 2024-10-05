import pytest
import socket

from pydis.client import RedisClient


@pytest.fixture
def client():
    client = RedisClient()
    client.flushall()
    yield client
    client.flushall()


def test_command_keys_all(client):
    client.set("my_key", "")
    assert len(client.keys("*")) == 1
