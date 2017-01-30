import random


class Square():
    def __init__(self, mine=False, revealed=False):
        self.mine = mine
        self.revealed = revealed
        self.mines_adjacent = 0
        self.flag = False

    def __str__(self):
        if self.revealed:
            if self.mine:
                return '*'
            else:
                return str(self.mines_adjacent)
        elif self.flag:
            return "/"
        else:
            return " "

class MineSweeper():
    def __init__(self, size=8, mines=10):
        self.size = size
        self.mines = mines
        self.board = [] 
        self.clicked_yet = False
        self.game_over = False
        self.won = False
        self.mines_coordinates = []
        for _ in range(self.size):
            self.board.append([Square() for _ in range(self.size)])

    def flag(self, x, y):
        if x < 0 or x > self.size-1 or y < 0 or y > self.size-1 or self.board[x][y].revealed:
            return
        elif self.board[x][y].flag:
            self.board[x][y].flag = False
        else:
            self.board[x][y].flag = True

    def click(self, x, y):
        """
        Handles effects of clicking a square with coordinates x and y.
        """
        if not x < self.size or not y < self.size:
            return
        if self.clicked_yet:
            if self.board[x][y].mine:
                self.reveal_mines()
                self.game_over = True
            elif not self.board[x][y].revealed:
                self.reveal_squares(x, y)
                self.check_won()
            self.refresh_board()
        else:
            self.populate_board(x, y)
            self.clicked_yet = True
            self.click(x, y)


    def populate_board(self, x_in, y_in):
        """
        Populates board with mines based off of first square clicked with coordinates x,y.
        """

        for _ in range(self.mines):
            x = random.randint(0, self.size-1)
            y = random.randint(0, self.size-1)
            while self.board[x][y].mine or ((x_in-1 <= x <= x_in+1)  and ( y_in-1 <= y <= y_in + 1)):
                x = random.randint(0, self.size-1)
                y = random.randint(0, self.size-1)
            self.board[x][y].mine = True
            self.mines_coordinates.append((x,y))
        self.get_adjacent_mines()

    def get_adjacent_mines(self):
        """
        Tallies the number of mines adjacent to each square.
        """
        for x, y in self.mines_coordinates:
            self.add_mine_count(x-1,y-1)
            self.add_mine_count(x-1,y)
            self.add_mine_count(x-1,y+1)
            self.add_mine_count(x,y-1)
            self.add_mine_count(x,y+1)
            self.add_mine_count(x+1,y-1)
            self.add_mine_count(x+1,y)
            self.add_mine_count(x+1,y+1)

    def add_mine_count(self, x, y):
        """
        If coordinate exists on board and square isn't a mine adds 1 to mines_adjacent count.
        """
        if x < 0 or x > self.size-1 or y < 0 or y > self.size-1 or self.board[x][y].mine: 
            #return if IndexError or already revealed
            return
        else:
            self.board[x][y].mines_adjacent += 1


    def reveal_squares(self, x, y):
        """
        If coordinates exists on board recursively reveals squares until squares with adjacent mines are hit.
        """
        if x < 0 or x > self.size-1 or y < 0 or y > self.size-1 or self.board[x][y].revealed: 
            #return if IndexError or already revealed
            return
        if self.board[x][y].mines_adjacent:
            self.board[x][y].revealed = True
        else:
            #If square has no adjacent bombs recursively reveal all adjacent squares.
            self.board[x][y].revealed = True
            self.reveal_squares(x-1,y-1)
            self.reveal_squares(x-1,y)
            self.reveal_squares(x-1,y+1)
            self.reveal_squares(x,y-1)
            self.reveal_squares(x,y+1)
            self.reveal_squares(x+1,y-1)
            self.reveal_squares(x+1,y)
            self.reveal_squares(x+1,y+1)

    def reveal_mines(self):
        """
        Reveals all mines on the board.
        """
        for x, y in self.mines_coordinates:
            self.board[x][y].revealed = True

    def refresh_board(self):
        pass

    def check_won(self):
        """
        Checks if board is fully revealed (win condition met).
        """
        for row in self.board:
            for s in row:
                if not s.revealed and not s.mine:
                    return
        self.won = True

    def __str__(self):
        s = " "
        for i in range(self.size):
            s+= f"{i},"
        s = s[:-1] + "\n"
        for i, line in enumerate(self.board):
            s += "["
            for sqr in line:
                s += str(sqr)
                s += ","
            s = s[:-1] + f"]{i}\n"
        return s


def main():
    ms = MineSweeper(20, 50)
    print(ms)
    while not ms.game_over or ms.won:
        flag = input("flag or click (f or c): \n") == "f"
        try:
            x, y = [int(x) for x in input("Coordinates separated by comma:\n").split(",")]
            if flag:
                ms.flag(x,y)
            else:
                ms.click(x,y)
        except:
            pass
        
        print(ms)
    if ms.game_over:
        print("Game Over!")
    else:
        print("You won!")

if __name__ == "__main__":
    main()


