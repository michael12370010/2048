import tkinter as tk
import colors as c
import random


class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048")
        
        self.cell_grid = tk.Frame(
            self, bg=c.GRID_COLOR, bd=3, width=600, height=600
        )
        self.cell_grid.grid(pady=(100, 0))
        self.master.resizable(False, False) 
        self.GUI()
        self.start_game()
        
        self.master.bind("<Left>", self.kiri)
        self.master.bind("<Right>", self.kanan)
        self.master.bind("<Up>", self.atas)
        self.master.bind("<Down>", self.bawah)

        self.mainloop()


    def GUI(self):
        #Grid 
        self.cells =[]
        for horizontal in range(4):
            row = []
            for vertical in range(4):
                cell_frame = tk.Frame(
                    self.cell_grid,
                    bg=c.EMPTY_COLOR,
                    width=150,
                    height=150
                )
                cell_frame.grid(row=horizontal, column=vertical, padx=5, pady=5)
                cell_number = tk.Label(self.cell_grid, bg=c.EMPTY_COLOR)
                cell_number.grid(row=horizontal, column=vertical)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        #Score header
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=45, anchor="center")
        tk.Label(
            score_frame,
            text="Score",
            font=c.SCORE_LABEL_FONT
        ).grid(row=0)
        self.score_label = tk.Label(score_frame, text="0", font=c.SCORE_FONT)
        self.score_label.grid(row=1)


    def start_game(self):
        # create matrix of zeroes
        self.matrix = [[0]*4 for _ in range(4)]

        # fill a random cells with 2s
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=c.CELL_COLORS[2],
            fg=c.NUMBER_COLORS[2],
            font=c.NUMBER_FONTS[2],
            text="2"
        )

        self.score = 0


    #matrix manipulation function
    def stack(self):
        new_matrix = [[0]*4 for _ in range(4)]
        for horizontal in range(4):
            fill_position = 0
            for vertical in range(4):
                if self.matrix[horizontal][vertical] !=0:
                    new_matrix[horizontal][fill_position] = self.matrix[horizontal][vertical]
                    fill_position += 1
        self.matrix = new_matrix


    def combine(self):
        for horizontal in range(4):
            for vertical in range(3):
                if self.matrix[horizontal][vertical] !=0 and self.matrix[horizontal][vertical] == self.matrix[horizontal][vertical +1]:
                    self.matrix[horizontal][vertical] *= 2
                    self.matrix[horizontal][vertical + 1] = 0
                    self.score += self.matrix[horizontal][vertical]


    def reverse(self):
        new_matrix = []
        for horizontal in range(4):
            new_matrix.append([])
            for vertical in range(4):
                new_matrix[horizontal].append(self.matrix[horizontal][3 - vertical])
        self.matrix = new_matrix


    def transpose(self):
        new_matrix = [[0]*4 for _ in range(4)]
        for horizontal in range(4):
            for vertical in range(4):
                new_matrix[horizontal][vertical] = self.matrix[vertical][horizontal]
        self.matrix = new_matrix


    # add a new 2 or 4 tile randomly to an empty cell

    def add_new_tile(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        while(self.matrix[row][col] !=0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = random.choice([2, 4])


    #update the GUI to match the matrix

    def update_GUI(self):
        for horizontal in range(4):
            for vertical in range(4):
                cell_value = self.matrix[horizontal][vertical]
                if cell_value == 0:
                    self.cells[horizontal][vertical]["frame"].configure(bg=c.EMPTY_COLOR)
                    self.cells[horizontal][vertical]["number"].configure(bg=c.EMPTY_COLOR, text="")
                else:
                    self.cells[horizontal][vertical]["frame"].configure(bg=c.CELL_COLORS[cell_value])
                    self.cells[horizontal][vertical]["number"].configure(
                        bg=c.CELL_COLORS[cell_value],
                        fg=c.NUMBER_COLORS[cell_value],
                        font=c.NUMBER_FONTS[cell_value],
                        text=str(cell_value)
                    )
        self.score_label.configure(text=self.score)
        self.update_idletasks()


    # Check if any moves are possible

    def horizontal_move_exists(self):
        for horizontal in range(4):
            for vertical in range(3):
                if self.matrix[horizontal][vertical] == self.matrix[horizontal][vertical + 1]:
                    return True
        return False

    def vertical_move_exists(self):
        for horizontal in range(3):
            for vertical in range(4):
                if self.matrix[horizontal][vertical] == self.matrix[horizontal + 1][vertical]:
                    return True
        return False


    # Check if game is over (Win/Lose)

    def game_over(self):
        if any(2048 in row for row in self.matrix):
            game_over_frame = tk.Frame(self.cell_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="You Win!",
                bg=c.WINNER_BG,
                fg=c.GAME_OVER_COLOR,
                font=c.GAME_OVER_FONT
            ).pack()
        elif not any(0 in row for row in self.matrix) and not self.horizontal_move_exists() and not self.vertical_move_exists():
            game_over_frame = tk.Frame(self.cell_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="Game Over!",
                bg=c.LOSER_BG ,
                fg=c.GAME_OVER_COLOR,
                font=c.GAME_OVER_FONT
            ).pack()
            
    # Arrow press function

    def kiri(self, event):
        self.stack()
        self.combine()
        self.stack()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def kanan(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def atas(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def bawah(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

Game()
