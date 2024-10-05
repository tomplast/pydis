import asyncio
import warnings

try:
    pass
except:
    warnings.warn("uvloop not available, falling back to asyncio loop")


_data = {}


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

    def _run_GET(self, data):
        global _data

        if not data in _data:
            self._transport.write(b"$-1\r\n")
            return

        d = _data[data]

        self._transport.write(f"${len(d)}\r\n{d}\r\n".encode())

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
