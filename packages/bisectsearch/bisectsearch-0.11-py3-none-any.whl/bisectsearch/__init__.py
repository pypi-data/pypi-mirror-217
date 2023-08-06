from bisect import bisect_left, bisect_right


def rightmost_value_equal_to(a, x):
    """
    Returns the index of the rightmost occurrence of the value x in the sorted list a.

    Args:
        a (list): A sorted list of values.
        x: The value to search for.

    Returns:
        int or None: The index of the rightmost occurrence of x if found, None otherwise.
    """
    i = bisect_right(a, x)
    if i <= len(a) and a[i - 1] == x:
        return i - 1
    return None


def leftmost_value_equal_to(a, x):
    """
    Returns the index of the leftmost occurrence of the value x in the sorted list a.

    Args:
        a (list): A sorted list of values.
        x: The value to search for.

    Returns:
        int or None: The index of the leftmost occurrence of x if found, None otherwise.
    """
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    return None


def rightmost_value_less_than(a, x):
    """
    Returns the index of the rightmost value in the sorted list a that is less than x.

    Args:
        a (list): A sorted list of values.
        x: The reference value.

    Returns:
        int or None: The index of the rightmost value less than x if found, None otherwise.
    """
    i = bisect_left(a, x)
    if i:
        return i - 1
    return None


def rightmost_value_less_than_or_equal(a, x):
    """
    Returns the index of the rightmost value in the sorted list a that is less than or equal to x.

    Args:
        a (list): A sorted list of values.
        x: The reference value.

    Returns:
        int or None: The index of the rightmost value less than or equal to x if found, None otherwise.
    """
    i = bisect_right(a, x)
    if i:
        return i - 1
    return None


def leftmost_value_greater_than(a, x):
    """
    Returns the index of the leftmost value in the sorted list a that is greater than x.

    Args:
        a (list): A sorted list of values.
        x: The reference value.

    Returns:
        int or None: The index of the leftmost value greater than x if found, None otherwise.
    """
    i = bisect_right(a, x)
    if i != len(a):
        return i
    return None


def leftmost_value_greater_than_or_equal(a, x):
    """
    Returns the index of the leftmost value in the sorted list a that is greater than or equal to x.

    Args:
        a (list): A sorted list of values.
        x: The reference value.

    Returns:
        int or None: The index of the leftmost value greater than or equal to x if found, None otherwise.
    """
    i = bisect_left(a, x)
    if i != len(a):
        return i
    return None


