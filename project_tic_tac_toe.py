import tkinter as tk
import random

class TicTacToe:
    def __init__(self, root, size=5, multiplayer=False):
        self.root = root
        self.size = size
        self.board = [["" for _ in range(size)] for _ in range(size)]
        self.current_player = "X"
        self.multiplayer = multiplayer
        self.buttons = []

        self.create_board()
        self.restart_button = tk.Button(root, text="Restart",font=("Times New Roman", 24, "bold"), command=self.restart, state=tk.DISABLED, fg="red")
        self.restart_button.grid(row=size, columnspan=size)
        self.result_label = tk.Label(root, text="", font=("Times New Roman", 24, "bold"), fg="lime green")
        self.result_label.grid(row=size + 1, columnspan=size)
        self.root.mainloop()

    def create_board(self):
        for i in range(self.size):
            row = []
            for j in range(self.size):
                button = tk.Button(
                    self.root,
                    text="",
                    width=6,
                    height=3,
                    font=("Times New Roman", 24, "bold"),
                    command=lambda i=i, j=j: self.make_move(i, j),
                    state=tk.NORMAL,
                )
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

        if not self.multiplayer and self.current_player == "O":
            self.ai_move()

    def make_move(self, row, col):
        if self.board[row][col] == "" and not self.check_winner():
            self.board[row][col] = self.current_player

            # Set font color for X and O
            font_color = "blue" if self.current_player == "X" else "red"
            self.buttons[row][col].config(text=self.current_player, state=tk.DISABLED, fg=font_color)

            if self.check_winner():
                self.display_winner(self.current_player)
            elif all(self.board[i][j] != "" for i in range(self.size) for j in range(self.size)):
                self.display_winner("Tie")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.current_player == "O" and not self.multiplayer:
                    self.ai_move()

    def ai_move(self):
        empty_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == ""]
        if empty_cells:
            ai_move = random.choice(empty_cells)
            self.make_move(ai_move[0], ai_move[1])

    def check_winner(self):
        def check_consecutive(lst, player, consecutive):
            count = 0
            for val in lst:
                if val == player:
                    count += 1
                    if count == consecutive:
                        return True
                else:
                    count = 0
            return False

        # Check rows, columns, and diagonals
        for i in range(self.size):
            if (
                check_consecutive(self.board[i], "X", 4) or check_consecutive(self.board[i], "O", 4) or
                check_consecutive([self.board[j][i] for j in range(self.size)], "X", 4) or
                check_consecutive([self.board[j][i] for j in range(self.size)], "O", 4)
            ):
                return True

        for i in range(self.size):
            for j in range(self.size):
                if (
                    i <= self.size - 4 and
                    check_consecutive([self.board[i + k][j] for k in range(4)], self.current_player, 4)
                ):
                    return True
                if (
                    j <= self.size - 4 and
                    check_consecutive([self.board[i][j + k] for k in range(4)], self.current_player, 4)
                ):
                    return True
                if (
                    i <= self.size - 4 and j <= self.size - 4 and
                    check_consecutive([self.board[i + k][j + k] for k in range(4)], self.current_player, 4)
                ):
                    return True
                if (
                    i <= self.size - 4 and j >= 3 and
                    check_consecutive([self.board[i + k][j - k] for k in range(4)], self.current_player, 4)
                ):
                    return True

        return False

    def display_winner(self, winner):
        if winner == "Tie":
            self.result_label.config(text="It's a Tie!")
        else:
            self.result_label.config(text=f"{winner} is the winner!")
        self.restart_button.config(state=tk.NORMAL)

    def restart(self):
        for i in range(self.size):
            for j in range(self.size):
                self.board[i][j] = ""
                self.buttons[i][j].config(text="", state=tk.NORMAL)
        self.current_player = "X"
        self.result_label.config(text="")
        self.restart_button.config(state=tk.DISABLED)

def start_multiplayer_game():
    root = tk.Tk()
    root.title("Tic Tac Toe (Multiplayer)")
    game = TicTacToe(root, size=5, multiplayer=True)

def start_single_player_game():
    root = tk.Tk()
    root.title("Tic Tac Toe (Single Player)")
    game = TicTacToe(root, size=5, multiplayer=False)

# Main menu
menu_root = tk.Tk()
menu_root.title("Tic Tac Toe - Main Menu")
menu_label = tk.Label(menu_root, text="Choose a Game Mode:", font=("Times New Roman", 16, "bold"))
menu_label.pack()

# Set background color of buttons to light sky blue
multiplayer_button = tk.Button(menu_root, text="Multiplayer", command=start_multiplayer_game, bg="light sky blue", font=("Times New Roman", 12, "bold"))
multiplayer_button.pack()

single_player_button = tk.Button(menu_root, text="Single Player", command=start_single_player_game, bg="light sky blue", font=("Times New Roman", 12, "bold"))
single_player_button.pack()

menu_root.mainloop()
