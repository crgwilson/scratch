from cloud_sync import RemoteBlobStore, bytes_to_string, sync


def test_sync_uploads_every_local_key_to_remote() -> None:
    remote = RemoteBlobStore()

    sync({"a": "alpha", "b": "beta"}, remote)

    assert bytes_to_string(remote.get("a")) == "alpha"
    assert bytes_to_string(remote.get("b")) == "beta"


def test_sync_overwrites_existing_remote_values() -> None:
    remote = RemoteBlobStore()
    sync({"a": "first"}, remote)

    sync({"a": "second"}, remote)

    assert bytes_to_string(remote.get("a")) == "second"


# Part 2 - only changed keys
#
# def test_sync_only_uploads_changed_keys() -> None:
#     remote = CountingRemoteBlobStore()
#     sync({"a": "alpha"}, remote)
#     sync({"a": "alpha", "b": "beta"}, remote)
#
#     assert remote.put_count_by_key == {"a": 1, "b": 1}
#
#
# Part 3 - partial upload failure
#
# def test_partial_failure_can_be_retried_without_corrupting_remote() -> None:
#     ...
#
#
# Part 4 - concurrent writers
#
# def test_conflicting_client_write_is_detected() -> None:
#     ...
#
#
# Part 5 - persistent key-value store
#
# def test_persistent_store_recovers_after_reopen(tmp_path) -> None:
#     path = tmp_path / "store.log"
#     store = PersistentKeyValueStore(str(path))
#     store.put("a", "alpha")
#     store.close()
#
#     reopened = PersistentKeyValueStore(str(path))
#
#     assert reopened.get("a") == "alpha"
#
#
# Part 6 - partial log record recovery
#
# def test_recovery_ignores_partial_trailing_record(tmp_path) -> None:
#     ...
