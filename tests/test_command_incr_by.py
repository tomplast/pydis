import pytest
import socket

from pydis.client import RedisClient


@pytest.fixture
def client():
    client = RedisClient()
    client.flushall()
    yield client
    client.flushall()


def test_command_incr_by_with_no_data(client):
    assert client.incrby("no_data", 100) == 100


def test_command_incr_by_with_data(client):
    client.set("some_data", "1")
    assert client.incrby("some_data", 10) == 11


def test_command_incr_by_with_wrong_data(client):
    client.set("some_data", '"NOT A NUMBER"')
    with pytest.raises(Exception):
        client.incrby("some_data", 10)
