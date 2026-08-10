# P2 - Resumable iterator over a large dataset
#
# Part 1:
# * consume a source that yields items in batches.
# * next(iterator) returns one item at a time across batch boundaries.
#
# Part 2:
# * checkpoint() returns an opaque token.
# * resume(token) continues exactly where it left off.
#
# Part 3:
# * handle the source throwing mid-batch with no duplicated and no dropped items.
#
# Part 4:
# * make resume work when the underlying source has shrunk since the checkpoint.
class ResumableIterator:
    def __init__(self, source) -> None:
        self.source = source

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedError

    def checkpoint(self) -> str:
        raise NotImplementedError

    @classmethod
    def resume(cls, source, token: str) -> "ResumableIterator":
        raise NotImplementedError
