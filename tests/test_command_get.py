import pytest
import socket

from pydis.client import RedisClient


@pytest.fixture
def client():
    client = RedisClient()
    client.flushall()
    yield client
    client.flushall()


def test_command_get_with_no_data(client):
    assert client.get("no_data") is None


def test_command_get_with_data(client):
    client.set("some_data", '"THERE_IS_DATA_HERE"')
    assert client.get("some_data") == "THERE_IS_DATA_HERE"
