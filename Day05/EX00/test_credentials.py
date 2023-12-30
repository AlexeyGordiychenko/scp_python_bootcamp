import requests
from urllib.parse import quote


def check(species, credentials, status=200):
    response = requests.get(f'http://127.0.0.1:8888/?species={quote(species)}')
    assert response.json() == {
        'credentials': credentials
    }
    assert response.status_code == status


def test_cyberman():
    check('Cyberman', 'John Lumic')


def test_dalek():
    check('Dalek', 'Davros')


def test_judoon():
    check('Judoon', 'Shadow Proclamation Convention 15 Enforcer')


def test_human():
    check('Human', 'Leonardo da Vinci')


def test_ood():
    check('Ood', 'Klineman Halpen')


def test_silence():
    check('Silence', 'Tasha Lem')


def test_slitheen():
    check('Slitheen', 'Coca-Cola salesman')


def test_sontaran():
    check('Sontaran', 'General Staal')


def test_time_lord():
    check('Time Lord', 'Rassilon')


def test_weeping_angel():
    check('Weeping Angel', 'The Division Representative')


def test_zygon():
    check('Zygon', 'Broton')


def test_unknown():
    check('Something', 'Unknown', 404)
