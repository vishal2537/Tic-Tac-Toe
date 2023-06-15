import tkinter as tk
import random
from tkinter import messagebox


class GameBoard:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.moves = 0

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.moves += 1

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def is_winner(self, player):
        for row in range(3):
            if self.board[row] == [player, player, player]:
                return True

        for col in range(3):
            if [self.board[0][col], self.board[1][col], self.board[2][col]] == [player, player, player]:
                return True

        if [self.board[0][0], self.board[1][1], self.board[2][2]] == [player, player, player]:
            return True

        if [self.board[2][0], self.board[1][1], self.board[0][2]] == [player, player, player]:
            return True

        return False

    def is_draw(self):
        return self.moves == 9

    def is_game_over(self):
        return self.is_winner('X') or self.is_winner('O') or self.is_draw()


class AIPlayer:
    def __init__(self):
        self.best_move = None

    def get_best_move(self, game, difficulty):
        self.best_move = None
        if difficulty == 0:
            depth = 6
        elif difficulty == 1:
            depth = 8
        else:
            depth = 20
        self.alpha_beta_algo(game, 0, float('-inf'), float('inf'), True, depth)
        if self.best_move is None:
            valid_moves = [(row, col) for row in range(3)
                           for col in range(3) if game.board[row][col] == ' ']
            if valid_moves:
                self.best_move = random.choice(valid_moves)
        return self.best_move

    def alpha_beta_algo(self, game, depth, alpha, beta, maximizing, max_depth):
        if depth == max_depth or game.is_game_over():
            if game.is_winner('X'):
                return -1
            elif game.is_winner('O'):
                return 1
            else:
                return 0

        if maximizing:
            max_eval = float('-inf')
            for row in range(3):
                for col in range(3):
                    if game.board[row][col] == ' ':
                        game.make_move(row, col)
                        eval = self.alpha_beta_algo(
                            game, depth + 1, alpha, beta, False, max_depth)
                        game.board[row][col] = ' '
                        game.moves -= 1
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            if depth == 0:
                self.best_move = self.get_best_move_from_evaluation_function(
                    game, max_eval)
            return max_eval
        else:
            min_eval = float('inf')
            for row in range(3):
                for col in range(3):
                    if game.board[row][col] == ' ':
                        game.make_move(row, col)
                        eval = self.alpha_beta_algo(
                            game, depth + 1, alpha, beta, True, max_depth)
                        game.board[row][col] = ' '
                        game.moves -= 1
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            if depth == 0:
                self.best_move = self.get_best_move_from_evaluation_function(
                    game, min_eval)
            return min_eval

    def get_best_move_from_evaluation_function(self, game, eval):
        valid_moves = [(row, col) for row in range(3)
                       for col in range(3) if game.board[row][col] == ' ']
        for move in valid_moves:
            game.make_move(move[0], move[1])
            if self.alpha_beta_algo(game, 1, float('-inf'), float('inf'), False, 1) == eval:
                game.board[move[0]][move[1]] = ' '
                game.moves -= 1
                return move
            game.board[move[0]][move[1]] = ' '
            game.moves -= 1
        return None


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.game = GameBoard()
        self.ai_player = AIPlayer()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.difficulty = 0

        self.board_frame = tk.Frame(self.root, bg="green")
        self.board_frame.grid(row=0, column=0)

        for row in range(3):
            for col in range(3):
                self.buttons[row][col] = tk.Button(
                    self.root,
                    text="",
                    font=("Arial", 20),
                    width=10,
                    height=4,
                    command=lambda row=row, col=col: self.make_move(row, col), bg="lightblue"
                )
                self.buttons[row][col].grid(row=row, column=col)

        self.exit_button = tk.Button(
            self.root,
            text="Exit",
            font=("Arial", 14),
            width=5,
            # bg="lightgray",
            command=self.root.quit
        )
        self.exit_button.grid(row=3, column=2, columnspan=3, pady=5)

        self.difficulty_button = tk.Button(
            self.root,
            text="Difficulty: Easy",
            font=("Arial", 14),
            width=15,
            # bg="lightgray",
            command=self.change_difficulty
        )
        self.difficulty_button.grid(row=3, columnspan=2, pady=5)

    def make_move(self, row, col):
        if self.game.board[row][col] == ' ' and not self.game.is_game_over():
            self.buttons[row][col].config(text=self.game.current_player)
            self.game.make_move(row, col)
            self.game.switch_player()
            if self.game.is_winner('X'):
                self.game_over_message("Player X wins!")
            elif self.game.is_winner('O'):
                self.game_over_message("Player O wins!")
            elif self.game.is_draw():
                self.game_over_message("It's a draw!")
            else:
                self.ai_make_move()

    def ai_make_move(self):
        if not self.game.is_game_over():
            move = self.ai_player.get_best_move(self.game, self.difficulty)
            self.game.make_move(move[0], move[1])
            self.buttons[move[0]][move[1]].config(
                text=self.game.current_player)
            if self.game.is_winner(self.game.current_player):
                self.game_over_message(
                    f"Player {self.game.current_player} wins!")
            elif self.game.is_draw():
                self.game_over_message("It's a draw!")
            else:
                self.game.switch_player()

    def game_over_message(self, message):
        if self.game.is_winner('X') or self.game.is_winner('O'):
            messagebox.showinfo("Game Over", message)
        else:
            messagebox.showinfo("Game Over", "It's a draw!")
        self.reset_game()

    def reset_game(self):
        self.game = GameBoard()
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="")

    def change_difficulty(self):
        if self.difficulty == 0:
            self.difficulty = 1
            self.difficulty_button.config(text="Difficulty: Medium")
        elif self.difficulty == 1:
            self.difficulty = 2
            self.difficulty_button.config(text="Difficulty: Hard")
        else:
            self.difficulty = 0
            self.difficulty_button.config(text="Difficulty: Easy")


root = tk.Tk()
tictactoegui = TicTacToeGUI(root)
root.mainloop()
