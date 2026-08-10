from resumable_iterator import ResumableIterator


class BatchSource:
    def __init__(self, batches: list[list[int]]) -> None:
        self.batches = batches

    def batches_from(self, start_batch: int = 0):
        for batch in self.batches[start_batch:]:
            yield batch


def test_iterates_items_across_batch_boundaries() -> None:
    iterator = ResumableIterator(BatchSource([[1, 2], [], [3], [4, 5]]))

    assert list(iterator) == [1, 2, 3, 4, 5]


def test_empty_source_is_exhausted() -> None:
    iterator = ResumableIterator(BatchSource([]))

    assert list(iterator) == []


# Part 2 - checkpoint/resume
#
# def test_resume_continues_after_checkpoint() -> None:
#     source = BatchSource([[1, 2], [3, 4]])
#     iterator = ResumableIterator(source)
#
#     assert next(iterator) == 1
#     token = iterator.checkpoint()
#     resumed = ResumableIterator.resume(source, token)
#
#     assert list(resumed) == [2, 3, 4]
#
#
# Part 3 - source throws mid-batch
#
# def test_retry_after_source_error_has_no_duplicate_or_dropped_items() -> None:
#     ...
#
#
# Part 4 - source shrank
#
# def test_resume_from_shrunken_source_stops_cleanly() -> None:
#     ...
