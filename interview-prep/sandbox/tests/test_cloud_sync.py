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
