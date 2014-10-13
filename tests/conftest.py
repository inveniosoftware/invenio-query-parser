import pytest


def generate_tests(generate_test):
    def fun(cls):
        for count, (query, expected) in enumerate(cls.queries):
            func = generate_test(query, expected)
            func.__name__ = 'test_%s' % count
            func.__doc__ = "Parsing query %s" % query
            setattr(cls, func.__name__, func)
        return cls
    return fun


def pytest_namespace():
    return dict((
        ("generate_tests", generate_tests),
    ))