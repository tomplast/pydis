import asyncio
import warnings
import random

try:
    pass
except:
    warnings.warn("uvloop not available, falling back to asyncio loop")


_data = {}
_last_successful_db_timestamp = 0


class RedisProtocol(asyncio.Protocol):
    def __init__(self, event):
        self._shutdown_event = event

    def connection_made(self, transport):
        self._transport = transport

    def data_received(self, data):
        parts = (
            data.decode("ascii")
            .replace("\n", "")
            .replace("\r", "")
            .split(" ", maxsplit=1)
        )

        command = parts[0]
        data = ""
        if len(parts) == 2:
            data = parts[-1]

        if f"_run_{command}" in dir(self):
            getattr(self, f"_run_{command}")(data)
        else:
            self._transport.write(
                (
                    "-ERR unknown command '" + command + "', with args beginning with:"
                ).encode()
            )

    def _run_SADD(self, arguments):
        global _data
        key, members = arguments.split(" ", maxsplit=1)

        if key not in _data:
            _data[key] = set()

        changed_count = 0

        if type(_data[key]) is not set:
            self._transport.write(
                b"-WRONGTYPE Operation against a key holding the wrong kind of value\r\n"
            )
            return

        for member in members.split(" "):
            if key not in _data[key]:
                changed_count += 1
                _data[key].add(member)

        self._transport.write(f":{changed_count}\r\n".encode())

    def _run_SHUTDOWN(self, data):
        self._shutdown_event.set()
        self._transport.close()

    def _run_ECHO(self, data):
        if len(data) == 0:
            self._transport.write(
                b"-ERR wrong number of arguments for 'echo' command\r\n"
            )
            return

        self._transport.write(
            f"${len(data) - 2}\r\n".encode("ascii") + data.encode("ascii")
        )

    def _run_DECRBY(self, arguments):
        global _data
        key, value = "", ""

        if '"' in arguments:
            key, value = arguments.split('"', maxsplit=1)
            key = key.rstrip(" ")
            value = value.rstrip('"')
        else:
            key, value = arguments.split(" ")

        value = int(value)

        if key not in _data:
            _data[key] = -value
        else:
            if not _data[key].isdigit():
                self._transport.write(
                    b"-ERR value is not an integer or out of range\r\n"
                )
                return

            _data[key] = int(_data[key]) - value
        self._transport.write(f":{_data[key]}\r\n".encode("ascii"))

    def _run_INCRBY(self, arguments):
        global _data
        key, value = "", ""

        if '"' in arguments:
            key, value = arguments.split('"', maxsplit=1)
            key = key.rstrip(" ")
            value = value.rstrip('"')
        else:
            key, value = arguments.split(" ")

        value = int(value)

        if key not in _data:
            _data[key] = value
        else:
            if not _data[key].isdigit():
                self._transport.write(
                    b"-ERR value is not an integer or out of range\r\n"
                )
                return

            _data[key] = int(_data[key]) + value
        self._transport.write(f":{_data[key]}\r\n".encode("ascii"))

    def _run_DEL(self, arguments):
        global _data
        for k in arguments.split(" "):
            if k in _data:
                del _data[k]

        self._transport.write(b"+OK\r\n")

    def _run_DECR(self, key):
        global _data
        if key not in _data:
            _data[key] = -1
        else:
            if not _data[key].isdigit():
                self._transport.write(
                    b"-ERR value is not an integer or out of range\r\n"
                )
                return

            _data[key] = int(_data[key]) - 1
        self._transport.write(f":{_data[key]}\r\n".encode("ascii"))

    def _run_INCR(self, key):
        global _data
        if key not in _data:
            _data[key] = 1
        else:
            if not _data[key].isdigit():
                self._transport.write(
                    b"-ERR value is not an integer or out of range\r\n"
                )
                return

            _data[key] = int(_data[key]) + 1

        self._transport.write(f":{_data[key]}\r\n".encode("ascii"))

    def _run_QUIT(self, data):
        self._transport.close()

    def _run_FLUSHALL(self, data):
        global _data
        _data = {}
        self._transport.write(b"+OK\r\n")

    def _run_SET(self, data):
        global _data
        key, value = "", ""

        if '"' in data:
            key, value = data.split('"', maxsplit=1)
            key = key.rstrip(" ")
            value = value.rstrip('"')
        else:
            key, value = data.split(" ")

        print(f">{key}<")
        print(f"<{value}>")

        _data[key] = value

        self._transport.write(b"+OK\r\n")

    def _run_EXISTS(self, key):
        if key in _data:
            self._transport.write(b":1\r\n")
        else:
            self._transport.write(b":0\r\n")

    def _run_GET(self, data):
        global _data

        if not data in _data:
            self._transport.write(b"$-1\r\n")
            return

        d = _data[data]

        self._transport.write(f"${len(d)}\r\n{d}\r\n".encode())

    def _run_RANDOMKEY(self, _):
        if len(_data) == 0:
            self._transport.write(b"$-1\r\n")
            return

        random_key = random.choice(_data)

        self._transport.write(f"${len(random_key)}\r\n{random_key}\r\n".encode())

    def _run_LASTSAVE(self, _):
        self._transport.write(f":{_last_successful_db_timestamp}\r\n".encode("ascii"))

    def _run_KEYS(self, pattern):
        if pattern != "*":
            raise NotImplementedError("Only * supported")

        keys = [x for x in _data.keys()]

        response = f"*{len(keys)}\r\n"
        for k in keys:
            response += f"${len(k)}\r\n{k}\r\n"

        self._transport.write(response.encode("ascii"))

    def _run_PING(self, data):
        if len(data) > 0:
            self._transport.write(
                f"${len(data)}".encode("ascii")
                + b"\r\n"
                + data.encode("ascii")
                + b"\r\n"
            )
            return
        self._transport.write(b"+PONG\r\n")


async def main():
    loop = asyncio.get_event_loop()
    shutdown_event = asyncio.Event()
    server = await loop.create_server(
        lambda: RedisProtocol(shutdown_event), "localhost", 6379
    )
    await shutdown_event.wait()
    server.close()
    await server.wait_closed()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped")
