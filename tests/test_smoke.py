def test_import_and_version():
    import contraction
    assert hasattr(contraction, "__version__")
