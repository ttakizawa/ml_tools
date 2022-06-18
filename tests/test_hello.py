from ml_tools.hello import hello


def test_hello(capfd):
    hello()

    out, err = capfd.readouterr()
    assert out == "hello\n"
    assert err is ''