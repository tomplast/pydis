import pytest
import socket

from pydis.client import RedisClient


@pytest.fixture
def client():
    client = RedisClient()
    client.flushall()
    yield client
    client.flushall()


def test_command_random_key_without_data(client):
    assert client.random_key() == ""


def test_command_random_key_with_data(client):
    client.set("some_data", '"THERE_IS_DATA_HERE"')
    assert client.random_key() is not None
