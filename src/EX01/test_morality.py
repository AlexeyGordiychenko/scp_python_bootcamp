from morality import *


def test_cheater():
    player = Cheater()
    assert player.play() == "cheat"
    player.update("cheat")
    assert player.play() == "cheat"
    player.update("cooperate")
    assert player.play() == "cheat"


def test_cooperator():
    player = Cooperator()
    assert player.play() == "cooperate"
    player.update("cheat")
    assert player.play() == "cooperate"
    player.update("cooperate")
    assert player.play() == "cooperate"


def test_copycat():
    player = Copycat()
    assert player.play() == "cooperate"
    player.update("cheat")
    assert player.play() == "cheat"
    player.update("cooperate")
    assert player.play() == "cooperate"


def test_grudger_cheat():
    player = Grudger()
    assert player.play() == "cooperate"
    player.update("cooperate")
    assert player.play() == "cooperate"
    player.update("cheat")
    assert player.play() == "cheat"
    player.update("cooperate")
    assert player.play() == "cheat"


def test_grudger_no_cheat():
    player = Grudger()
    assert player.play() == "cooperate"
    player.update("cooperate")
    assert player.play() == "cooperate"
    player.update("cooperate")
    assert player.play() == "cooperate"
    player.update("cooperate")
    assert player.play() == "cooperate"


def test_detective_cheater():
    player = Detective()
    assert player.play() == "cooperate"
    player.update("cooperate")
    assert player.play() == "cheat"
    player.update("cooperate")
    assert player.play() == "cooperate"
    player.update("cooperate")
    assert player.play() == "cooperate"
    player.update("cooperate")
    assert player.play() == "cheat"
    player.update("cooperate")
    assert player.play() == "cheat"
    player.update("cooperate")
    assert player.play() == "cheat"


def test_detective_copycat_1():
    player = Detective()
    assert player.play() == "cooperate"
    player.update("cooperate")
    assert player.play() == "cheat"
    player.update("cooperate")
    assert player.play() == "cooperate"
    player.update("cooperate")
    assert player.play() == "cooperate"
    player.update("cheat")
    assert player.play() == "cheat"
    player.update("cooperate")
    assert player.play() == "cooperate"
    player.update("cheat")
    assert player.play() == "cheat"


def test_detective_copycat_2():
    player = Detective()
    assert player.play() == "cooperate"
    player.update("cheat")
    assert player.play() == "cheat"
    player.update("cooperate")
    assert player.play() == "cooperate"
    player.update("cheat")
    assert player.play() == "cooperate"
    player.update("cooperate")
    assert player.play() == "cooperate"
    player.update("cheat")
    assert player.play() == "cheat"
    player.update("cooperate")
    assert player.play() == "cooperate"


def test_evilcopycat():
    player = EvilCopycat()
    assert player.play() == "cheat"
    player.update("cooperate")
    assert player.play() == "cooperate"
    player.update("cheat")
    assert player.play() == "cheat"


def test_game_default():
    game = Game()
    players = [Cheater(), Cooperator(), Copycat(),
               Grudger(), Detective()]
    for player1, player2 in itertools.combinations(players, 2):
        game.play(player1, player2)

    assert dict(game.registry) == {
        'copycat': 57, 'grudger': 46, 'cheater': 45, 'detective': 45, 'cooperator': 29}


def test_game_one_round():
    game = Game(1)
    players = [Cheater(), Cooperator(), Copycat(),
               Grudger(), Detective()]
    for player1, player2 in itertools.combinations(players, 2):
        game.play(player1, player2)

    assert dict(game.registry) == {
        'cheater': 12, 'cooperator': 5, 'copycat': 5, 'grudger': 5, 'detective': 5}


def test_game_default_new_player():
    game = Game()
    players = [Cheater(), Cooperator(), Copycat(),
               Grudger(), Detective(), EvilCopycat()]
    for player1, player2 in itertools.combinations(players, 2):
        game.play(player1, player2)

    assert dict(game.registry) == {'copycat': 67, 'detective': 60,
                                   'evilcopycat': 52, 'grudger': 48, 'cooperator': 46, 'cheater': 45}


def test_game_one_round_new_player():
    game = Game(1)
    players = [Cheater(), Cooperator(), Copycat(),
               Grudger(), Detective(), EvilCopycat()]
    for player1, player2 in itertools.combinations(players, 2):
        game.play(player1, player2)

    assert dict(game.registry) == {'cheater': 12, 'evilcopycat': 12,
                                   'cooperator': 4, 'copycat': 4, 'grudger': 4, 'detective': 4}
