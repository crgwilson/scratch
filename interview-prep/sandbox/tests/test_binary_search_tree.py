from binary_search_tree import BinarySearchTree


def build_tree() -> BinarySearchTree:
    tree = BinarySearchTree()
    for value in [5, 3, 7, 2, 4, 6, 8]:
        tree.insert(value)
    return tree


def test_empty_tree_queries() -> None:
    tree = BinarySearchTree()

    assert tree.root is None
    assert tree.contains(10) is False
    assert tree.inorder() == []
    assert tree.min() is None
    assert tree.max() is None
    assert tree.remove(10) is False


def test_insert_search_and_inorder_traversal() -> None:
    tree = build_tree()

    assert tree.contains(2) is True
    assert tree.contains(5) is True
    assert tree.contains(8) is True
    assert tree.contains(99) is False
    assert tree.inorder() == [2, 3, 4, 5, 6, 7, 8]
    assert tree.min() == 2
    assert tree.max() == 8


def test_duplicate_insert_is_ignored() -> None:
    tree = build_tree()

    tree.insert(4)
    tree.insert(5)

    assert tree.inorder() == [2, 3, 4, 5, 6, 7, 8]


def test_remove_leaf_node() -> None:
    tree = build_tree()

    assert tree.remove(2) is True

    assert tree.contains(2) is False
    assert tree.inorder() == [3, 4, 5, 6, 7, 8]


def test_remove_node_with_one_child() -> None:
    tree = BinarySearchTree()
    for value in [5, 3, 7, 2]:
        tree.insert(value)

    assert tree.remove(3) is True

    assert tree.contains(3) is False
    assert tree.inorder() == [2, 5, 7]


def test_remove_node_with_two_children() -> None:
    tree = build_tree()

    assert tree.remove(7) is True

    assert tree.contains(7) is False
    assert tree.inorder() == [2, 3, 4, 5, 6, 8]


def test_remove_root_until_tree_is_empty() -> None:
    tree = BinarySearchTree()
    for value in [2, 1, 3]:
        tree.insert(value)

    assert tree.remove(2) is True
    assert tree.inorder() == [1, 3]
    assert tree.remove(1) is True
    assert tree.inorder() == [3]
    assert tree.remove(3) is True

    assert tree.root is None
    assert tree.inorder() == []
