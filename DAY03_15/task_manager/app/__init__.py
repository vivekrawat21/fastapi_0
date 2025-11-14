"""Make `app` a regular package for tests and imports.

This project previously relied on implicit namespace packages. Adding
an explicit __init__ file ensures imports like `import app.main`
work consistently under pytest and different Python executions.
"""

__all__ = [
    "api",
    "core",
    "middleware",
    "repositories",
    "services",
    "utils",
]
