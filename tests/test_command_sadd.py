from decimal import DivisionByZero
import pytest
import socket

from pydis.client import RedisClient


@pytest.fixture
def client():
    client = RedisClient()
    client.flushall()
    yield client
    client.flushall()


def test_command_sadd_without_data(client):
    client.sadd("key1", ["member1", "member2"])
    assert client.exists("key1") == 1


def test_command_sadd_on_string(client):
    client.set("key1", "value")
    with pytest.raises(Exception):
        client.sadd("key1", ["member1", "member2"])
