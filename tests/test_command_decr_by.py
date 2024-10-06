import pytest
import socket

from pydis.client import RedisClient


@pytest.fixture
def client():
    client = RedisClient()
    client.flushall()
    yield client
    client.flushall()


def test_command_decr_by_with_no_data(client):
    assert client.decrby("no_data", 100) == -100


def test_command_decr_by_with_data(client):
    client.set("some_data", "1")
    assert client.decrby("some_data", 10) == -9


def test_command_decr_by_with_wrong_data(client):
    client.set("some_data", '"NOT A NUMBER"')
    with pytest.raises(Exception):
        client.decrby("some_data", 10)
