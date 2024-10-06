import pytest
import socket

from pydis.client import RedisClient


@pytest.fixture
def client():
    client = RedisClient()
    client.flushall()
    yield client
    client.flushall()


def test_command_decr_with_no_data(client):
    assert client.decr("no_data") == -1


def test_command_decr_with_data(client):
    client.set("some_data", "1")
    assert client.decr("some_data") == 0


def test_command_decr_with_wrong_data(client):
    client.set("some_data", '"NOT A NUMBER"')
    with pytest.raises(Exception):
        client.decr("some_data")
