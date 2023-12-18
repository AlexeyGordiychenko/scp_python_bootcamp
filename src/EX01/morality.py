from collections import Counter
import itertools


class Player:
    def cheat(self):
        return 'cheat'

    def cooperate(self):
        return 'cooperate'

    def play(self):
        pass

    def update(self, opponent_move):
        pass

    def reset(self):
        pass


class Cheater(Player):
    def play(self):
        return self.cheat()


class Cooperator(Player):
    def play(self):
        return self.cooperate()


class Copycat(Player):
    def __init__(self, last_opponent_move=None):
        self.last_opponent_move = last_opponent_move if last_opponent_move else self.cooperate()

    def play(self):
        return self.last_opponent_move

    def update(self, opponent_move):
        self.last_opponent_move = opponent_move

    def reset(self):
        self.__init__()


class Grudger(Player):
    def __init__(self):
        self.opponent_cheated = False

    def play(self):
        return self.cheat() if self.opponent_cheated else self.cooperate()

    def update(self, opponent_move):
        self.opponent_cheated = self.opponent_cheated or opponent_move == self.cheat()

    def reset(self):
        self.__init__()


class Detective(Player):
    def __init__(self):
        self.start_moves = [self.cooperate(), self.cheat(),
                            self.cooperate(), self.cooperate()]
        self.new_identity = None

    def play(self):
        if self.start_moves:
            move = self.start_moves.pop(0)
            return move
        else:
            move = self.new_identity.play()
            return move

    def update(self, opponent_move):
        if not self.new_identity:
            if opponent_move == self.cheat():
                self.new_identity = Copycat(opponent_move)
            elif not self.start_moves:
                self.new_identity = Cheater()
        else:
            self.new_identity.update(opponent_move)

    def reset(self):
        self.__init__()


class EvilCopycat(Copycat):
    def __init__(self):
        super().__init__(self.cheat())


class Game:
    def __init__(self, matches=10):
        self.matches = matches
        self.registry = Counter()

    def play(self, player1, player2):
        for _ in range(self.matches):
            move1 = player1.play()
            move2 = player2.play()
            result1, result2 = self._get_result(move1, move2)
            self.registry[player1.__class__.__name__.lower()] += result1
            self.registry[player2.__class__.__name__.lower()] += result2
            player1.update(move2)
            player2.update(move1)
        player1.reset()
        player2.reset()

    def _get_result(self, move1, move2):
        if move1 == 'cooperate' and move2 == 'cooperate':
            return 2, 2
        elif move1 == 'cooperate' and move2 == 'cheat':
            return -1, 3
        elif move1 == 'cheat' and move2 == 'cooperate':
            return 3, -1
        else:
            return 0, 0

    def top3(self):
        top3 = self.registry.most_common(3)
        for player, score in top3:
            print(f'{player} {score}')


if __name__ == "__main__":
    print('standard game:')
    game = Game()
    players = [Cheater(), Cooperator(), Copycat(),
               Grudger(), Detective()]
    for player1, player2 in itertools.combinations(players, 2):
        game.play(player1, player2)

    game.top3()

    print('with the new player:')
    game = Game()
    players = [Cheater(), Cooperator(), Copycat(),
               Grudger(), Detective(), EvilCopycat()]
    for player1, player2 in itertools.combinations(players, 2):
        game.play(player1, player2)

    game.top3()
