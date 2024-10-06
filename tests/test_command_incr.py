import pytest
import socket

from pydis.client import RedisClient


@pytest.fixture
def client():
    client = RedisClient()
    client.flushall()
    yield client
    client.flushall()


def test_command_incr_with_no_data(client):
    assert client.incr("no_data") == 1


def test_command_incr_with_data(client):
    client.set("some_data", "1")
    assert client.incr("some_data") == 2


def test_command_incr_with_wrong_data(client):
    client.set("some_data", '"NOT A NUMBER"')
    with pytest.raises(Exception):
        client.incr("some_data")
