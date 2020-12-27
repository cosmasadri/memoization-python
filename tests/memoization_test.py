from memoization import memoize


def test_memoize_function():
    return_value = 5
    test_function = lambda key: return_value

    memoized = memoize(test_function, 1000, lambda key: key)

    test_arg = "c544d3ae-a72d-4755-8ce5-d25db415b776"

    assert memoized(test_arg) == 5
