from energy import fix_wiring


def test_readme_1():
    plugs = ['plug1', 'plug2', 'plug3']
    sockets = ['socket1', 'socket2', 'socket3', 'socket4']
    cables = ['cable1', 'cable2', 'cable3', 'cable4']
    assert list(fix_wiring(cables, sockets, plugs)) == [
        'plug cable1 into socket1 using plug1',
        'plug cable2 into socket2 using plug2',
        'plug cable3 into socket3 using plug3',
        'weld cable4 to socket4 without plug'
    ]


def test_readme_2():
    plugs = ['plugZ', None, 'plugY', 'plugX']
    sockets = [1, 'socket1', 'socket2', 'socket3', 'socket4']
    cables = ['cable2', 'cable1', False]
    assert list(fix_wiring(cables, sockets, plugs)) == [
        'plug cable2 into socket1 using plugZ',
        'plug cable1 into socket2 using plugY'
    ]


def test_empty_plugs():
    plugs = []
    sockets = [1, 'socket1', 'socket2', 'socket3', 'socket4']
    cables = ['cable2', 'cable1', False, 'cableX']
    assert list(fix_wiring(cables, sockets, plugs)) == [
        'weld cable2 to socket1 without plug',
        'weld cable1 to socket2 without plug',
        'weld cableX to socket3 without plug'
    ]


def test_empty_sockets():
    plugs = ['plugZ', None, 'plugY', 'plugX']
    sockets = []
    cables = ['cable2', 'cable1', False, 'cableX']
    assert list(fix_wiring(cables, sockets, plugs)) == []


def test_empty_cables():
    plugs = ['plugZ', None, 'plugY', 'plugX']
    sockets = [1, 'socket1', 'socket2', 'socket3', 'socket4']
    cables = []
    assert list(fix_wiring(cables, sockets, plugs)) == []


def test_extra_plugs():
    plugs = ['plugZ', None, 'plugY', 'plugX', 'plugA', 'plugB']
    sockets = [1, 'socket1', 'socket2', 'socket3']
    cables = ['cable2', 'cable1', False, 'cableX']
    assert list(fix_wiring(cables, sockets, plugs)) == [
        'plug cable2 into socket1 using plugZ',
        'plug cable1 into socket2 using plugY',
        'plug cableX into socket3 using plugX',
    ]
