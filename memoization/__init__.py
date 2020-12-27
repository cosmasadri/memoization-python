from threading import Timer


def remove_key(key, cache_dict):
    del cache_dict[key]


def memoize(func, timeout, resolver=None):
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
