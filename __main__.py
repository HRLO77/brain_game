import importlib
try:
    main = importlib.import_module('main')
except Exception:
    import extra