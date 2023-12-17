from key import Key


def test_key():
    key = Key()
    assert len(key) == 1337
    assert key[404] == 3
    assert (key > 9000) == True
    assert key.passphrase == "zax2rulez"
    assert str(key) == "GeneralTsoKeycard"
