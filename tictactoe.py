from easyAI import TwoPlayerGame, AI_Player, Negamax
from easyAI.Player import Human_Player

class GameController(TwoPlayerGame):
    def __init__(self, players):
        self.players = players
        self.current_player = 1  # easyAI sử dụng current_player thay vì nplayer
        self.board = [0] * 9

    def possible_moves(self):
        return [a + 1 for a, b in enumerate(self.board) if b == 0]

    def make_move(self, move):
        self.board[int(move) - 1] = self.current_player

    def loss_condition(self):
        possible_combinations = [(1, 2, 3), (4, 5, 6), (7, 8, 9),
                                (1, 4, 7), (2, 5, 8), (3, 6, 9),
                                (1, 5, 9), (3, 5, 7)]
        # Sử dụng current_player và tính opponent đúng cách
        opponent = 3 - self.current_player
        return any(all(self.board[i - 1] == opponent
                       for i in combination)
                   for combination in possible_combinations)

    def is_over(self):
        return self.possible_moves() == [] or self.loss_condition()

    def show(self):
        print('\n'.join([' '.join(['.' if b == 0 else ('X' if b == 1 else 'O')
                                  for b in self.board[i*3:(i+1)*3]])
                         for i in range(3)]))

    def scoring(self):
        return -100 if self.loss_condition() else 0

if __name__ == "__main__":
    # Sử dụng Negamax với độ sâu 7
    algorithm = Negamax(7)
    game = GameController([Human_Player(), AI_Player(algorithm)])
    game.play()