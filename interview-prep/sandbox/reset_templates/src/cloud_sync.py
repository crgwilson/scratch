# P6 - Sync local state to cloud
#
# Given helpers that convert strings <-> bytes, sync a key/value store to a remote blob store.
#
# Part 1:
# * upload every local key/value pair to remote.
#
# Part 2:
# * only send changed keys.
#
# Part 3:
# * handle partial upload failure.
#
# Part 4:
# * handle two clients writing concurrently.
def string_to_bytes(value: str) -> bytes:
    return value.encode("utf-8")


def bytes_to_string(value: bytes) -> str:
    return value.decode("utf-8")


class RemoteBlobStore:
    def __init__(self) -> None:
        self.blobs: dict[str, bytes] = {}

    def put(self, key: str, value: bytes) -> None:
        self.blobs[key] = value

    def get(self, key: str) -> bytes | None:
        return self.blobs.get(key)


def sync(local: dict[str, str], remote: RemoteBlobStore) -> None:
    raise NotImplementedError
