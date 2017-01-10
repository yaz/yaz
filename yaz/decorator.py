def decorator(decorator_func):
    """Allows a decorator to be called with or without keyword arguments."""
    assert callable(decorator_func), type(decorator_func)

    def _decorator(func=None, **kwargs):
        assert func is None or callable(func), type(func)
        if func:
            return decorator_func(func, **kwargs)
        else:
            def _decorator_helper(func):
                return decorator_func(func, **kwargs)

            return _decorator_helper

    return _decorator

# @decorator
# def cache(func, ignore=None, type='memory', sqlite_filename='~/.yaz-cache.sqlite'):
#     assert ignore is None or isinstance(ignore, (tuple, list)), type(ignore)

#     def generate_key(args, kwargs):
#         # todo: do not cache when args and kwargs are not collections.Hashable (i.e. when we can not
#         # generate a proper key)
#         return (args, tuple(sorted((key, value) for key, value in kwargs.items() if not key in ignore)))

#     @functools.wraps(func)
#     def cache_from_memory(self, *args, **kwargs):
#         key = generate_key(args, kwargs)
#         hit = key in cache
#         if self.yaz.verbose:
#             print(self.render("{% color '', '', 'reverse' %}--- {{ plugin.__class__.__name__ }} {{ task.__name__ }} {{ cache }}{% endcolor %} {{ sourcefile }}",
#                               dict(plugin=self, task=func, sourcefile=inspect.getsourcefile(func), cache="CACHE HIT" if hit else "CACHE MISS")))
#         if not hit:
#             cache[key] = func(self, *args, **kwargs)
#         return cache[key]

#     @functools.wraps(func)
#     def cache_from_sqlite(self, *args, **kwargs):
#         key = generate_key(args, kwargs)
#         hit = key in cache
#         if self.yaz.verbose:
#             print(self.render("{% color '', '', 'reverse' %}--- {{ plugin.__class__.__name__ }} {{ task.__name__ }} {{ cache }}{% endcolor %} {{ sourcefile }}",
#                               dict(plugin=self, task=func, sourcefile=inspect.getsourcefile(func), cache="CACHE HIT" if hit else "CACHE MISS")))
#         if not hit:
#             cache[key] = func(self, *args, **kwargs)
#         return cache[key]

#     if type == 'memory':
#         cache = dict()
#         return cache_from_memory

#     if type == 'sqlite':
#         return cache_from_sqlite

#     raise RuntimeException('The parameter type must be either "memory" or "sqlite"')
