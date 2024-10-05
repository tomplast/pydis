import pytest
import socket

from pydis.client import RedisClient


@pytest.fixture
def client():
    return RedisClient()


def test_command_quit(client):
    client.quit()
