import socket


class RedisClient:
    def __init__(self):
        pass

    def _send_and_receive(self, command, arguments):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 6379))
        sock.send(command.encode() + (" " + arguments).encode() + b"\r\n")
        response = sock.recv(1024)
        sock.close()

        return response

    def command_is_available(self, command, data=""):
        command_in_upper = command.upper()

        response = self._send_and_receive(command_in_upper + " " + data, "")

        if b"ERR unknown command" in response:
            return False

        return True

    def echo(self, data):
        if not data.startswith('"'):
            data = '"' + data
        if not data.endswith('"'):
            data = data + '"'

        arguments = data.split("\r\n")

        response = self._send_and_receive("ECHO", data).decode("ascii")
        arguments = response.split("\r\n")

        if arguments[0].startswith("-ERR"):
            raise Exception(arguments[0])

        assert int(arguments[0][1:]) == len(data) - 2

        arguments[1] = arguments[1].strip('"')
        return arguments[1]

    def exists(self, data) -> int:
        response = self._send_and_receive("EXISTS", data).decode("ascii")
        arguments = response.split("\r\n")

        existing_count = int(arguments[0][1:])
        return existing_count

    def flushall(self, data=""):
        response = self._send_and_receive("FLUSHALL", data).decode("ascii")

        # FIX!
        assert "+OK" in response

    def set(self, key, value):
        if not value.startswith('"'):
            value = f'"{value}"'
        response = self._send_and_receive("SET", key + " " + value).decode("ascii")
        assert "+OK" in response

    def get(self, key):
        global _data
        response = self._send_and_receive("GET", key).decode("ascii")

        arguments = response.split("\r\n")

        if arguments[0] == "$-1":
            return None

        return arguments[1]

    def last_save(self):
        response = self._send_and_receive("LASTSAVE", "").decode("ascii")
        arguments = response.split("\r\n")
        return int(arguments[0][1:])

    def keys(self, pattern):
        response = self._send_and_receive("KEYS", pattern).decode("ascii")
        arguments = response.split("\r\n")

        number_of_arguments = int(arguments[0][1:])

        if number_of_arguments == 0:
            return []

        keys = []
        for i in range(2, len(arguments) - 1, 2):
            keys.append(arguments[i])

        return keys

    def quit(self):
        return self._send_and_receive("QUIT", "")

    def ping(self, data=""):
        response = self._send_and_receive("PING", data).decode("ascii")
        arguments = response.split("\r\n")

        if len(data) > 0:
            assert int(arguments[0][1:]) == len(data)
            arguments[1] = arguments[1].strip('"')
            return arguments[1]

        return arguments[0]
