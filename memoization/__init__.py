from threading import Timer


def remove_key(key, cache_dict):
    del cache_dict[key]


def memoize(func, timeout, resolver=None):
    """
    Creates a function that memoizes the result of func. If resolver is provided,
    it determines the cache key for storing the result based on the arguments provided to the memorized function.
    By default, the first argument provided to the memorized function is used as the map cache key. The memorized values
    timeout after the timeout exceeds. The timeout is in defined in milliseconds.

    Example:
    function addToTime(year, month, day) {
     return Date.now() + Date(year, month, day);
    }

    const memoized = memoization.memoize(addToTime, (year, month, day) => year + month + day, 5000)

    // call the provided function cache the result and return the value
    const result = memoized(1, 11, 26); // result = 1534252012350

    // because there was no timeout this call should return the memorized value from the first call
    const secondResult = memoized(1, 11, 26); // secondResult = 1534252012350

    // after 5000 ms the value is not valid anymore and the original function should be called again
    const thirdResult = memoized(1, 11, 26); // thirdResult = 1534252159271

    Args:
        func (function): the function for which the return values should be cached
        timeout (float || int): if provided gets called for each function call with the exact same set of parameters
        as the original function, the resolver function should provide the memoization key.
        resolver (function, optional): timeout for cached values in milliseconds. Defaults to None.
    """
    cache = dict()

    if type(timeout) != int and type(timeout) != float:
        raise TypeError("timeout must be integer or float")
    else:
        # converting from milliseconds into seconds
        timeout = timeout / 1000

    if not callable(func):
        raise TypeError("func must be a function")

    if resolver is not None and not callable(resolver):
        raise TypeError("resolver must be a function")

    def memoized_func(*args):
        cache_key = str(args) if resolver is None else resolver(*args)

        if cache_key in cache:
            return cache[cache_key]

        result = func(*args)
        cache[cache_key] = result

        Timer(timeout, remove_key, (cache_key, cache)).start()
        return result

    return memoized_func
