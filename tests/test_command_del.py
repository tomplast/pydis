import pytest
import socket

from pydis.client import RedisClient


@pytest.fixture
def client():
    client = RedisClient()
    client.flushall()
    yield client
    client.flushall()


def test_command_del_with_data(client):
    client.set("key1", "key1")
    client.delete(["key1"])
    assert client.exists("key1") == 0


def test_command_del_with_data_keeping_unrelated_key(client):
    client.set("key1", "key1")
    client.set("key2", "key2")
    client.delete(["key1"])
    assert client.exists("key2") == 1
