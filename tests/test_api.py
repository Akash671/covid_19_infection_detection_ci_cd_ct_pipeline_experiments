import importlib

def test_api_import():
    api_module = importlib.import_module("api.main")
    assert api_module is not None
