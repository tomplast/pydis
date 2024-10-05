import pytest
import socket

from pydis.client import RedisClient


@pytest.fixture
def client():
    client = RedisClient()
    client.flushall()
    yield client
    client.flushall()


def test_command_last_save(client):
    assert type(client.last_save()) is int
