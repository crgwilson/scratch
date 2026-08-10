from itertools import islice

from ip_address_iterator import CIDRIterator


def test_iterates_all_addresses_in_small_cidr_block() -> None:
    assert list(CIDRIterator("192.168.1.0/30")) == [
        "192.168.1.0",
        "192.168.1.1",
        "192.168.1.2",
        "192.168.1.3",
    ]


def test_single_address_cidr_block() -> None:
    assert list(CIDRIterator("10.0.0.1/32")) == ["10.0.0.1"]


# Part 2 - multiple blocks without duplicates
#
# def test_overlapping_blocks_are_deduplicated() -> None:
#     assert list(MultiCIDRIterator(["10.0.0.0/30", "10.0.0.2/31"])) == [
#         "10.0.0.0",
#         "10.0.0.1",
#         "10.0.0.2",
#         "10.0.0.3",
#     ]
#
#
# Part 3 - lazy and memory-flat
#
# def test_large_block_is_lazy() -> None:
#     iterator = iter(CIDRIterator("10.0.0.0/8"))
#
#     assert list(islice(iterator, 3)) == ["10.0.0.0", "10.0.0.1", "10.0.0.2"]
