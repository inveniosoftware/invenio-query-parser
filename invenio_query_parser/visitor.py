# Stores the actual visitor methods
def make_visitor():
    _methods = {}

    # The actual @visitor decorator
    def _visitor(arg_type):
        """Decorator that creates a visitor method."""

        # Delegating visitor implementation

        def _visitor_impl(self, arg, *args, **kwargs):
            """Actual visitor method implementation."""
            method = _methods[type(arg)]
            return method(self, arg, *args, **kwargs)

        def decorator(fn):
            _methods[arg_type] = fn
            # Replace all decorated methods with _visitor_impl
            return _visitor_impl

        return decorator

    return _visitor
