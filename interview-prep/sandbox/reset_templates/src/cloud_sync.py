# P6 - Sync local state to cloud / persistent key-value store
#
# Given helpers that convert strings <-> bytes, sync a key/value store to a remote blob store.
# Reported variants of this prompt often skew toward persistent key-value storage,
# append-only logs, snapshots, partial-write recovery, and concurrent writers.
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
#
# Part 5:
# * persist local state with an append-only log and recover after restart.
#
# Part 6:
# * detect and recover from a partial/corrupt log record.
def string_to_bytes(value: str) -> bytes:
    return value.encode("utf-8")


def bytes_to_string(value: bytes) -> str:
    return value.decode("utf-8")


class RemoteBlobStore:
    def __init__(self) -> None:
        raise NotImplementedError

    def put(self, key: str, value: bytes) -> None:
        raise NotImplementedError

    def get(self, key: str) -> bytes | None:
        raise NotImplementedError


def sync(local: dict[str, str], remote: RemoteBlobStore) -> None:
    raise NotImplementedError


class PersistentKeyValueStore:
    def __init__(self, path: str) -> None:
        raise NotImplementedError

    def put(self, key: str, value: str) -> None:
        raise NotImplementedError

    def get(self, key: str) -> str | None:
        raise NotImplementedError

    def delete(self, key: str) -> None:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError
