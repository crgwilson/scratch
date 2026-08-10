# P8 - IP address iterator
#
# Part 1:
# * iterate every address in a CIDR block.
#
# Part 2:
# * support multiple overlapping blocks without duplicates.
#
# Part 3:
# * make iteration lazy and memory-flat for a /8.
class CIDRIterator:
    def __init__(self, cidr: str) -> None:
        self.cidr = cidr

    def __iter__(self):
        raise NotImplementedError


class MultiCIDRIterator:
    def __init__(self, cidrs: list[str]) -> None:
        self.cidrs = cidrs

    def __iter__(self):
        raise NotImplementedError
