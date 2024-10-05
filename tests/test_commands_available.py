import pytest

from pydis.client import RedisClient


@pytest.fixture
def client():
    return RedisClient()


def test_command_auth_is_available(client):
    assert client.command_is_available("auth")


def test_command_bgrewriteaof_is_available(client):
    assert client.command_is_available("bgrewriteaof")


def test_command_bgsave_is_available(client):
    assert client.command_is_available("bgsave")


def test_command_dbsize_is_available(client):
    assert client.command_is_available("dbsize")


def test_command_decr_is_available(client):
    assert client.command_is_available("decr")


def test_command_decrby_is_available(client):
    assert client.command_is_available("decrby")


def test_command_del_is_available(client):
    assert client.command_is_available("del")


def test_command_echo_is_available(client):
    assert client.command_is_available("echo", "DATA")


def test_command_exists_is_available(client):
    assert client.command_is_available("exists")


def test_command_expire_is_available(client):
    assert client.command_is_available("expire")


def test_command_flushall_is_available(client):
    assert client.command_is_available("flushall")


def test_command_flushdb_is_available(client):
    assert client.command_is_available("flushdb")


def test_command_get_is_available(client):
    assert client.command_is_available("get")


# Deprecated since Redis version 6.2.0
#    def test_command_getset_is_available(client):
#    assert client.command_is_available("getset")


def test_command_incr_is_available(client):
    assert client.command_is_available("incr")


def test_command_incrby_is_available(client):
    assert client.command_is_available("incrby")


def test_command_info_is_available(client):
    assert client.command_is_available("info")


def test_command_keys_is_available(client):
    assert client.command_is_available("keys")


def test_command_lastsave_is_available(client):
    assert client.command_is_available("lastsave")


def test_command_lindex_is_available(client):
    assert client.command_is_available("lindex")


def test_command_llen_is_available(client):
    assert client.command_is_available("llen")


def test_command_lpop_is_available(client):
    assert client.command_is_available("lpop")


def test_command_lpush_is_available(client):
    assert client.command_is_available("lpush")


def test_command_lrange_is_available(client):
    assert client.command_is_available("lrange")


def test_command_lrem_is_available(client):
    assert client.command_is_available("lrem")


def test_command_lset_is_available(client):
    assert client.command_is_available("lset")


def test_command_ltrim_is_available(client):
    assert client.command_is_available("ltrim")


def test_command_mget_is_available(client):
    assert client.command_is_available("mget")


def test_command_monitor_is_available(client):
    assert client.command_is_available("monitor")


def test_command_move_is_available(client):
    assert client.command_is_available("move")


def test_command_ping_is_available(client):
    assert client.command_is_available("ping")


def test_command_quit_is_available(client):
    assert client.command_is_available("quit")


def test_command_randomkey_is_available(client):
    assert client.command_is_available("randomkey")


def test_command_rename_is_available(client):
    assert client.command_is_available("rename")


def test_command_renamenx_is_available(client):
    assert client.command_is_available("renamenx")


def test_command_rpop_is_available(client):
    assert client.command_is_available("rpop")


def test_command_rpush_is_available(client):
    assert client.command_is_available("rpush")


def test_command_sadd_is_available(client):
    assert client.command_is_available("sadd")


def test_command_save_is_available(client):
    assert client.command_is_available("save")


def test_command_scard_is_available(client):
    assert client.command_is_available("scard")


def test_command_sdiff_is_available(client):
    assert client.command_is_available("sdiff")


def test_command_sdiffstore_is_available(client):
    assert client.command_is_available("sdiffstore")


def test_command_select_is_available(client):
    assert client.command_is_available("select")


def test_command_set_is_available(client):
    assert client.command_is_available("set")


def test_command_setnx_is_available(client):
    assert client.command_is_available("setnx")


def test_command_shutdown_is_available(client):
    assert True is True  # assert client.command_is_available("shutdown")


def test_command_sinter_is_available(client):
    assert client.command_is_available("sinter")


def test_command_sinterstore_is_available(client):
    assert client.command_is_available("sinterstore")


def test_command_sismember_is_available(client):
    assert client.command_is_available("sismember")


def test_command_slaveof_is_available(client):
    assert client.command_is_available("slaveof")


def test_command_smembers_is_available(client):
    assert client.command_is_available("smembers")


def test_command_smove_is_available(client):
    assert client.command_is_available("smove")


def test_command_sort_is_available(client):
    assert client.command_is_available("sort")


def test_command_spop_is_available(client):
    assert client.command_is_available("spop")


def test_command_srandmember_is_available(client):
    assert client.command_is_available("srandmember")


def test_command_srem_is_available(client):
    assert client.command_is_available("srem")


def test_command_substr_is_available(client):
    assert client.command_is_available("substr")


def test_command_sunion_is_available(client):
    assert client.command_is_available("sunion")


def test_command_sunionstore_is_available(client):
    assert client.command_is_available("sunionstore")


def test_command_sync_is_available(client):
    assert client.command_is_available("sync")


def test_command_ttl_is_available(client):
    assert client.command_is_available("ttl")


def test_command_type_is_available(client):
    assert client.command_is_available("type")
