import time
from unittest.mock import Mock, patch

import pytest
from memoization import memoize


def test_memoize_function_result():
    """
    Memoize function should memoize function result
    """
    return_value = 5
    test_function = lambda key: return_value

    memoized = memoize(test_function, 10, lambda key: key)

    test_arg = "c544d3ae-a72d-4755-8ce5-d25db415b776"

    assert memoized(test_arg) == 5

    return_value = 10

    assert memoized(test_arg) == 5


def test_memoize_function_result_without_resolver():
    """
    Memoize function should memoize function result without resolver
    """
    return_value = 5
    test_function = lambda key: return_value

    memoized = memoize(test_function, 10)

    test_arg = "c544d3ae-a72d-4755-8ce5-d25db415b776"

    assert memoized(test_arg) == 5

    return_value = 10

    assert memoized(test_arg) == 5


def test_memoize_function_result_different_argument():
    """
    Memoize function should memoize function result with defferent argument
    """
    return_value = 5

    test_function = lambda key: return_value

    mock_test_function = Mock(wraps=test_function)
    memoized = memoize(mock_test_function, 10, lambda key: key)

    assert mock_test_function.call_count == 0

    test_arg_1 = "c544d3ae-a72d-4755-8ce5-d25db415b776"

    assert memoized(test_arg_1) == 5
    assert mock_test_function.call_count == 1

    return_value = 10

    assert memoized(test_arg_1) == 5
    assert mock_test_function.call_count == 1

    test_arg_2 = "c544d3ae-a72d-4755-8ce5"

    assert memoized(test_arg_2) == 10
    assert mock_test_function.call_count == 2


def test_return_memoized_result_before_timeout():
    """
    Memoize function should retrieve memoized result if timeout is not exceeded
    (function should not be called)
    """
    return_value = 5

    test_function = lambda key: return_value

    mock_test_function = Mock(wraps=test_function)
    memoized = memoize(mock_test_function, 1000, lambda key: key)

    assert mock_test_function.call_count == 0

    test_arg = "c544d3ae-a72d-4755-8ce5-d25db415b776"

    assert memoized(test_arg) == 5
    assert mock_test_function.call_count == 1

    time.sleep(0.9)
    assert memoized(test_arg) == 5
    assert mock_test_function.call_count == 1


def test_remove_memoized_result_after_timeout():
    """
    Memoize function should remove memoized result if timeout is exceeded
    (function must be called again to get result)
    """
    return_value = 5

    test_function = lambda key: return_value

    mock_test_function = Mock(wraps=test_function)
    memoized = memoize(mock_test_function, 1000, lambda key: key)

    assert mock_test_function.call_count == 0

    test_arg = "c544d3ae-a72d-4755-8ce5-d25db415b776"

    assert memoized(test_arg) == 5
    assert mock_test_function.call_count == 1

    time.sleep(1)
    assert memoized(test_arg) == 5
    assert mock_test_function.call_count == 2


def test_error_timeout_argument():
    """
    Memoize function should throw error if given timeout argument is not a number
    """
    return_value = 5

    test_function = lambda key: return_value

    with pytest.raises(TypeError, match="timeout must be integer or float"):
        memoize(test_function, "error", lambda key: key)


def test_error_resolver_argument():
    """
    Memoize function should throw error if given func argument is not a function
    """
    return_value = 5

    test_function = lambda key: return_value

    with pytest.raises(TypeError, match="resolver must be a function"):
        memoize(test_function, 10, "error")


def test_error_func_argument():
    """
    Memoize function should throw error if given resolver argument is not a function
    """

    with pytest.raises(TypeError, match="func must be a function"):
        memoize("error", 10, lambda key: key)
