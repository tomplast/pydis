import pytest
import socket

from pydis.client import RedisClient


@pytest.fixture
def client():
    return RedisClient()


def test_command_flush_not_raises(client):
    client.flushall()
