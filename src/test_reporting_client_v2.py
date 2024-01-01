from reporting_client_v2 import Spaceship
import pytest


def test_corvette_correct1():
    assert Spaceship(alignment='Enemy', name='TestSpaceship',
                     class_='Corvette', length=80, crew_size=4, armed=True) is not None


def test_corvette_correct2():
    assert Spaceship(alignment='Ally', name='TestSpaceship',
                     class_='Corvette', length=250, crew_size=10, armed=False) is not None


def test_corvette_length_incorrect1():
    with pytest.raises(ValueError, match='Incorrect length for Corvette'):
        Spaceship(alignment='Enemy', name='TestSpaceship',
                  class_='Corvette', length=79, crew_size=4, armed=True)


def test_corvette_length_incorrect2():
    with pytest.raises(ValueError, match='Incorrect length for Corvette'):
        Spaceship(alignment='Ally', name='TestSpaceship',
                  class_='Corvette', length=251, crew_size=10, armed=False)


def test_corvette_crew_size_incorrect1():
    with pytest.raises(ValueError, match='Incorrect crew size for Corvette'):
        Spaceship(alignment='Enemy', name='TestSpaceship',
                  class_='Corvette', length=80, crew_size=3, armed=True)


def test_corvette_crew_size_incorrect2():
    with pytest.raises(ValueError, match='Incorrect crew size for Corvette'):
        Spaceship(alignment='Ally', name='TestSpaceship',
                  class_='Corvette', length=250, crew_size=11, armed=False)


def test_frigate_correct1():
    assert Spaceship(alignment='Ally', name='TestSpaceship',
                     class_='Frigate', length=300, crew_size=10, armed=True) is not None


def test_frigate_correct2():
    assert Spaceship(alignment='Ally', name='TestSpaceship',
                     class_='Frigate', length=600, crew_size=15, armed=False) is not None


def test_frigate_length_incorrect1():
    with pytest.raises(ValueError, match='Incorrect length for Frigate'):
        Spaceship(alignment='Ally', name='TestSpaceship',
                  class_='Frigate', length=299, crew_size=10, armed=True)


def test_frigate_length_incorrect2():
    with pytest.raises(ValueError, match='Incorrect length for Frigate'):
        Spaceship(alignment='Ally', name='TestSpaceship',
                  class_='Frigate', length=601, crew_size=15, armed=False)


def test_frigate_crew_size_incorrect1():
    with pytest.raises(ValueError, match='Incorrect crew size for Frigate'):
        Spaceship(alignment='Ally', name='TestSpaceship',
                  class_='Frigate', length=300, crew_size=9, armed=True)


def test_frigate_crew_size_incorrect2():
    with pytest.raises(ValueError, match='Incorrect crew size for Frigate'):
        Spaceship(alignment='Ally', name='TestSpaceship',
                  class_='Frigate', length=600, crew_size=16, armed=False)


def test_frigate_hostile():
    with pytest.raises(ValueError, match='Frigate can not be hostile'):
        Spaceship(alignment='Enemy', name='TestSpaceship',
                  class_='Frigate', length=300, crew_size=15, armed=True)


def test_cruiser_correct1():
    assert Spaceship(alignment='Ally', name='TestSpaceship',
                     class_='Cruiser', length=500, crew_size=15, armed=True) is not None


def test_cruiser_correct2():
    assert Spaceship(alignment='Enemy', name='TestSpaceship',
                     class_='Cruiser', length=1000, crew_size=30, armed=False) is not None


def test_cruiser_length_incorrect1():
    with pytest.raises(ValueError, match='Incorrect length for Cruiser'):
        Spaceship(alignment='Ally', name='TestSpaceship',
                  class_='Cruiser', length=499, crew_size=15, armed=True)


def test_cruiser_length_incorrect2():
    with pytest.raises(ValueError, match='Incorrect length for Cruiser'):
        Spaceship(alignment='Enemy', name='TestSpaceship',
                  class_='Cruiser', length=1001, crew_size=30, armed=False)


def test_cruiser_crew_size_incorrect1():
    with pytest.raises(ValueError, match='Incorrect crew size for Cruiser'):
        Spaceship(alignment='Ally', name='TestSpaceship',
                  class_='Cruiser', length=500, crew_size=14, armed=True)


def test_cruiser_crew_size_incorrect2():
    with pytest.raises(ValueError, match='Incorrect crew size for Cruiser'):
        Spaceship(alignment='Enemy', name='TestSpaceship',
                  class_='Cruiser', length=1000, crew_size=31, armed=False)


def test_destroyer_correct1():
    assert Spaceship(alignment='Ally', name='TestSpaceship',
                     class_='Destroyer', length=800, crew_size=50, armed=False) is not None


def test_destroyer_correct2():
    assert Spaceship(alignment='Ally', name='TestSpaceship',
                     class_='Destroyer', length=2000, crew_size=80, armed=True) is not None


def test_destroyer_length_incorrect1():
    with pytest.raises(ValueError, match='Incorrect length for Destroyer'):
        Spaceship(alignment='Ally', name='TestSpaceship',
                  class_='Destroyer', length=799, crew_size=50, armed=False)


def test_destroyer_length_incorrect2():
    with pytest.raises(ValueError, match='Incorrect length for Destroyer'):
        Spaceship(alignment='Ally', name='TestSpaceship',
                  class_='Destroyer', length=2001, crew_size=80, armed=True)


def test_destroyer_crew_size_incorrect1():
    with pytest.raises(ValueError, match='Incorrect crew size for Destroyer'):
        Spaceship(alignment='Ally', name='TestSpaceship',
                  class_='Destroyer', length=800, crew_size=49, armed=False)


def test_destroyer_crew_size_incorrect2():
    with pytest.raises(ValueError, match='Incorrect crew size for Destroyer'):
        Spaceship(alignment='Ally', name='TestSpaceship',
                  class_='Destroyer', length=2000, crew_size=81, armed=True)


def test_destroyer_hostile():
    with pytest.raises(ValueError, match='Destroyer can not be hostile'):
        Spaceship(alignment='Enemy', name='TestSpaceship',
                  class_='Destroyer', length=800, crew_size=80, armed=True)


def test_carrier_correct1():
    assert Spaceship(alignment='Enemy', name='TestSpaceship',
                     class_='Carrier', length=1000, crew_size=120, armed=False) is not None


def test_carrier_correct2():
    assert Spaceship(alignment='Ally', name='TestSpaceship',
                     class_='Carrier', length=4000, crew_size=250, armed=False) is not None


def test_carrier_length_incorrect1():
    with pytest.raises(ValueError, match='Incorrect length for Carrier'):
        Spaceship(alignment='Enemy', name='TestSpaceship',
                  class_='Carrier', length=999, crew_size=120, armed=False)


def test_carrier_length_incorrect2():
    with pytest.raises(ValueError, match='Incorrect length for Carrier'):
        Spaceship(alignment='Ally', name='TestSpaceship',
                  class_='Carrier', length=4001, crew_size=250, armed=False)


def test_carrier_crew_size_incorrect1():
    with pytest.raises(ValueError, match='Incorrect crew size for Carrier'):
        Spaceship(alignment='Enemy', name='TestSpaceship',
                  class_='Carrier', length=1000, crew_size=119, armed=False)


def test_carrier_crew_size_incorrect2():
    with pytest.raises(ValueError, match='Incorrect crew size for Carrier'):
        Spaceship(alignment='Ally', name='TestSpaceship',
                  class_='Carrier', length=4000, crew_size=251, armed=False)


def test_carrier_armed():
    with pytest.raises(ValueError, match='Carrier can not be armed'):
        Spaceship(alignment='Ally', name='TestSpaceship',
                  class_='Carrier', length=1000, crew_size=250, armed=True)


def test_dreadnought_correct1():
    assert Spaceship(alignment='Ally', name='TestSpaceship',
                     class_='Dreadnought', length=5000, crew_size=300, armed=True) is not None


def test_dreadnought_correct2():
    assert Spaceship(alignment='Enemy', name='TestSpaceship',
                     class_='Dreadnought', length=20000, crew_size=500, armed=False) is not None


def test_dreadnought_length_incorrect1():
    with pytest.raises(ValueError, match='Incorrect length for Dreadnought'):
        Spaceship(alignment='Ally', name='TestSpaceship',
                  class_='Dreadnought', length=4999, crew_size=300, armed=True)


def test_dreadnought_length_incorrect2():
    with pytest.raises(ValueError, match='Incorrect length for Dreadnought'):
        Spaceship(alignment='Enemy', name='TestSpaceship',
                  class_='Dreadnought', length=20001, crew_size=500, armed=False)


def test_dreadnought_crew_size_incorrect1():
    with pytest.raises(ValueError, match='Incorrect crew size for Dreadnought'):
        Spaceship(alignment='Ally', name='TestSpaceship',
                  class_='Dreadnought', length=5000, crew_size=299, armed=True)


def test_dreadnought_crew_size_incorrect2():
    with pytest.raises(ValueError, match='Incorrect crew size for Dreadnought'):
        Spaceship(alignment='Enemy', name='TestSpaceship',
                  class_='Dreadnought', length=20000, crew_size=501, armed=False)


def test_unknown_name_enemy():
    assert Spaceship(alignment='Enemy', name='Unknown',
                     class_='Dreadnought', length=20000, crew_size=500, armed=False) is not None


def test_unknown_name_ally():
    with pytest.raises(ValueError, match='Name \'Unknown\' can be only for enemy ships'):
        Spaceship(alignment='Ally', name='Unknown',
                  class_='Dreadnought', length=20000, crew_size=500, armed=False)
