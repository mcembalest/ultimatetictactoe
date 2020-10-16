BOARD = 'board'
EMPTY = 'empty'

class TicTacToeBoard:


    
    def __init__(self,data,row,col):
        self.row = row
        self.col = col
        self.fill_grid(data)
        self.winner = EMPTY_WINNER
        
    def fill_grid(self,data):
        if data == BOARD:
            self.grid = [ [TicTacToeBoard(EMPTY,i,j) for j in range(3)] for i in range(3)]
        else:
            self.grid = [ [data for j in range(3)] for i in range(3)]
            self.x_range, self.y_range = range(self.col*board_size,(self.col+1)*board_size), range(self.row*board_size,(self.row+1)*board_size)
        
    def place_piece(self,piece,row,col):
        self.grid[row][col] = piece
    
    def row_win(self,n):
        if self.grid[n][0]==self.grid[n][1] and self.grid[n][1]==self.grid[n][2] and self.grid[n][1] != EMPTY:
            self.winner = self.grid[n][1]
            return True
        return False
    
    def col_win(self,n):
        if self.grid[0][n]==self.grid[1][n] and self.grid[1][n]==self.grid[2][n] and self.grid[1][n] != EMPTY:
            self.winner = self.grid[1][n]
            return True
        return False
    
    def diag_win(self):
        if ((self.grid[0][0]==self.grid[1][1] and self.grid[1][1]==self.grid[2][2]) or (self.grid[2][0]==self.grid[1][1] and self.grid[1][1]==self.grid[0][2])) and self.grid[1][1] != EMPTY:
            self.winner = self.grid[1][1]
            return True
        return False
    
    def check_win(self):
        if self.winner is EMPTY_WINNER:
            if self.diag_win():
                return True
            for i in range(3):
                if self.row_win(i) or self.col_win(i):
                    return True
        return False
        
    def __eq__(self,other_board):
        return self.winner == other_board.winner and (self.winner != EMPTY_WINNER)
    
    def squares(self):
        return [self.grid[i][j] for i in range(3) for j in range(3)]