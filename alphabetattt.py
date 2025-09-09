from easyAI import TwoPlayerGame, AI_Player, Negamax
from easyAI.Player import Human_Player
import math

class GameController(TwoPlayerGame):
    def __init__(self, players):
        self.players = players
        self.current_player = 1  
        self.board = [0] * 9

    def possible_moves(self):
        return [a + 1 for a, b in enumerate(self.board) if b == 0]

    def make_move(self, move):
        self.board[int(move) - 1] = self.current_player

    def loss_condition(self):
        possible_combinations = [(1, 2, 3), (4, 5, 6), (7, 8, 9),
                                (1, 4, 7), (2, 5, 8), (3, 6, 9),
                                (1, 5, 9), (3, 5, 7)]
        
        opponent = 3 - self.current_player
        return any(all(self.board[i - 1] == opponent
                       for i in combination)
                   for combination in possible_combinations)

    def win_condition(self):
        possible_combinations = [(1, 2, 3), (4, 5, 6), (7, 8, 9),
                                (1, 4, 7), (2, 5, 8), (3, 6, 9),
                                (1, 5, 9), (3, 5, 7)]
        return any(all(self.board[i - 1] == self.current_player
                       for i in combination)
                   for combination in possible_combinations)

    def is_over(self):
        return self.possible_moves() == [] or self.loss_condition() or self.win_condition()

    def show(self):
        print('\n   |   |   ')
        print(' {} | {} | {} '.format(
            'X' if self.board[0] == 1 else 'O' if self.board[0] == 2 else '1',
            'X' if self.board[1] == 1 else 'O' if self.board[1] == 2 else '2',
            'X' if self.board[2] == 1 else 'O' if self.board[2] == 2 else '3'
        ))
        print('___|___|___')
        print('   |   |   ')
        print(' {} | {} | {} '.format(
            'X' if self.board[3] == 1 else 'O' if self.board[3] == 2 else '4',
            'X' if self.board[4] == 1 else 'O' if self.board[4] == 2 else '5',
            'X' if self.board[5] == 1 else 'O' if self.board[5] == 2 else '6'
        ))
        print('___|___|___')
        print('   |   |   ')
        print(' {} | {} | {} '.format(
            'X' if self.board[6] == 1 else 'O' if self.board[6] == 2 else '7',
            'X' if self.board[7] == 1 else 'O' if self.board[7] == 2 else '8',
            'X' if self.board[8] == 1 else 'O' if self.board[8] == 2 else '9'
        ))
        print('   |   |   ')

    def scoring(self):
        if self.win_condition():
            return 100
        elif self.loss_condition():
            return -100
        else:
            return 0


class AlphaBetaPruning:
    def __init__(self, depth=9):
        self.depth = depth
        self.nodes_explored = 0
        
    def __call__(self, game):
        self.nodes_explored = 0
        _, best_move = self.alphabeta(game, self.depth, -math.inf, math.inf, True)
        print(f"Nodes explored: {self.nodes_explored}")
        return best_move
    
    def alphabeta(self, game, depth, alpha, beta, maximizing_player):
        return self.max_value(game, depth, alpha, beta) if maximizing_player else self.min_value(game, depth, alpha, beta)
    
    def max_value(self, game, depth, alpha, beta):
       
        self.nodes_explored += 1
        
        if depth == 0 or game.is_over():
            return game.scoring(), None
        
        v = -math.inf
        best_move = None
        
        for move in game.possible_moves():
            game_copy = self.copy_game(game)
            game_copy.make_move(move)
            game_copy.current_player = 3 - game_copy.current_player
            
            min_val, _ = self.min_value(game_copy, depth - 1, alpha, beta)
            
            if min_val > v:
                v = min_val
                best_move = move
            
            if v >= beta:  # Beta cutoff
                return v, best_move
                
            alpha = max(alpha, v)
        
        return v, best_move
    
    def min_value(self, game, depth, alpha, beta):
        self.nodes_explored += 1
        
        if depth == 0 or game.is_over():
            return -game.scoring(), None  # Đảo dấu cho MIN player
        
        v = math.inf
        best_move = None
        
        for move in game.possible_moves():
            game_copy = self.copy_game(game)
            game_copy.make_move(move)
            game_copy.current_player = 3 - game_copy.current_player
            
            max_val, _ = self.max_value(game_copy, depth - 1, alpha, beta)
            
            if max_val < v:
                v = max_val
                best_move = move
            
            if v <= alpha:  # Alpha cutoff
                return v, best_move
                
            beta = min(beta, v)
        
        return v, best_move
    
    def copy_game(self, game):
        new_game = GameController(game.players)
        new_game.board = game.board.copy()
        new_game.current_player = game.current_player
        return new_game


class AlphaBetaPlayer:
    def __init__(self, depth=9):
        self.algorithm = AlphaBetaPruning(depth)
        
    def ask_move(self, game):
        return self.algorithm(game)


def play_game():
    print("Bạn là X (Player 1), AI là O (Player 2)")
    print("Nhập số từ 1-9 để đánh vào ô tương ứng:")
    
    game = GameController([Human_Player(), AlphaBetaPlayer(depth=9)])
    
    while not game.is_over():
        print(f"\n--- Lượt của Player {game.current_player} ---")
        game.show()
        
        if game.current_player == 1:
            try:
                move = int(input("Nhập nước đi của bạn (1-9): "))
                if move not in game.possible_moves():
                    print("Nước đi không hợp lệ! Hãy chọn ô trống.")
                    continue
            except ValueError:
                print("Vui lòng nhập số từ 1-9!")
                continue
        else:
            move = game.players[1].ask_move(game)
            # print(f"AI chọn ô {move}")
        
        game.make_move(move)
        game.current_player = 3 - game.current_player
    
    print("\n=== KẾT QUẢ GAME ===")
    game.show()
    
    game.current_player = 3 - game.current_player
    
    if game.win_condition():
        if game.current_player == 1:
            print("Bạn đã thắng!")
        else:
            print("Bạn đã thua!")
    else:
        print("Trò chơi hòa!")


if __name__ == "__main__":
    play_game()