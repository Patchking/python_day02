from abc import ABC, abstractmethod
from collections import Counter
from random import choice

# coop_or_no = {"coop": 0, "Cheat"}

class Player(ABC):
    def __init__(self, name: str, is_vindictive: bool = False):
        self._name = name
        self._is_vindictive = is_vindictive

    def update_op_bet(self, is_last_bet_coop: bool):
        pass

    def reset_player(self):
        pass

    def __str__(self):
        return self._name
    
    @abstractmethod
    def is_cooperate() -> bool:
        pass


class Cheater(Player):
    def is_cooperate(self):
        return False

class Coooper(Player):
    def is_cooperate(self):
        return True

class Copycat(Player):
    _is_last_bet_coop = True
    def update_op_bet(self, is_last_bet_coop: bool):
        self._is_last_bet_coop = is_last_bet_coop
    def is_cooperate(self):
        return self._is_last_bet_coop
    def reset_player(self):
        self._is_last_bet_coop = True

class SuperCopycat(Player):
    _is_last_bet_coop = True
    _cheater_flag = False
    def update_op_bet(self, is_last_bet_coop: bool):
        if not self._is_last_bet_coop and not is_last_bet_coop:
            self._cheater_flag = True
        self._is_last_bet_coop = is_last_bet_coop
    def is_cooperate(self):
        return not self._cheater_flag
    def reset_player(self):
        self._is_last_bet_coop = True
        self._cheater_flag = False

class Grudger(Player):
    _cheater_flag = False
    def update_op_bet(self, is_last_bet_coop: bool):
        if not is_last_bet_coop:
            self._cheater_flag = True
    def is_cooperate(self):
        return not self._cheater_flag
    def reset_player(self):
        self._cheater_flag = False
    

class Detective(Player):
    _start_sequence = [True, False, True, True]
    _cheater_flag = False
    _is_last_bet_coop = True
    def update_op_bet(self, is_last_bet_coop: bool):
        self._is_last_bet_coop = is_last_bet_coop
        if not is_last_bet_coop and self._start_sequence:
            self._cheater_flag = True
    def is_cooperate(self):
        if self._start_sequence:
            return self._start_sequence.pop(0)
        if self._cheater_flag:
            return self._is_last_bet_coop
        else:
            return False
    def reset_player(self):
        self._start_sequence = [True, False, True, True]
        self._cheater_flag = False
        self._is_last_bet_coop = True

class Game(object):

    def __init__(self, matches=10):
        self.matches = matches
        self.registry = Counter()

    def play(self, player1: Player, player2: Player):
        def reg_update(player, diff: int):
            self.registry[str(player)] += diff

        for i in range(self.matches):
            bet1 = player1.is_cooperate()
            bet2 = player2.is_cooperate()
            if bet1 == True and bet2 == True:
                player1.update_op_bet(True)
                player2.update_op_bet(True)
                reg_update(player1, +2)
                reg_update(player2, +2)
            elif bet1 == True and bet2 == False:
                player1.update_op_bet(False)
                player2.update_op_bet(True)
                reg_update(player1, -1)
                reg_update(player2, +3)
            elif bet1 == False and bet2 == True:
                player1.update_op_bet(True)
                player2.update_op_bet(False)
                reg_update(player1, +3)
                reg_update(player2, -1)
            else:
                player1.update_op_bet(False)
                player2.update_op_bet(False)
        player1.reset_player()
        player2.reset_player()

    def top3(self):
        common_list = self.registry.most_common(6)
        for i in range(len(common_list)):
            print(f"{i + 1}. {common_list[i][0]} {common_list[i][1]}")


class GameEngine():
    def __init__(self, extended_game: bool = False):
        self.possible_players = [Copycat("Copycat"), Cheater("Cheaeter"), Coooper("Cooper"), Grudger("Grudger"), Detective("Detective")]
        if extended_game:
            self.possible_players.append(SuperCopycat("SuperCopyCat"))
    def get_random_player(self):
        if not self.possible_players:
            raise Exception("Picked player from empty list")
        player = choice(self.possible_players)
        self.possible_players.remove(player)
        return player

    def start_game(self):
        list_of_players = [self.get_random_player() for i in range(len(self.possible_players))]

        size_of_list = len(list_of_players)
        game = Game()
        for i in range(size_of_list):
            for j in range(i + 1, size_of_list):
                game.play(list_of_players[i], list_of_players[j])
        game.top3()



def main():
    game = GameEngine(True)
    game.start_game()


if __name__ == "__main__":
    main()
