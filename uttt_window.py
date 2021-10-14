import tkinter as tk
import random

from uttt_game import TicTacToeBoard

#formatting constants
window_size = 600
shift = 50
duration = 1000
board_size = int(window_size/3)
sq_size = int(board_size/3)
background_color = 'blue'
piece_color = 'red'
board_outline_color = '#0de50d'
bg_tag = 'background'
pad = 10

#game constants
X = 'X'
O = 'O'
EMPTY = ''
EMPTY_WINNER = ''
BOARD = 'board'
    
class GameState:
    
    def __init__(self, prior_state, board_config, playable, winners):
        self.prior_state = prior_state
        self.board_config = board_config
        self.playable = playable
        self.winners = winners
    
    
class GameWindow(tk.Tk):
    
    def __init__(self):
        self.setup_game()
        self.setup_canvas()
        self.setup_click()
        self.setup_undo_button()
        
    def setup_canvas(self):
        tk.Tk.__init__(self)
        self.canvas = tk.Canvas(height=window_size,width=window_size)
        self.canvas.pack()
        self.draw_everything()
        
    def setup_game(self):
        self.mega_board = TicTacToeBoard(BOARD,None,None)
        self.piece = X
        self.playable_boards = self.mega_board.squares()
        self.winners = ['' for i in range(9)]
        self.state = GameState(None, [self.mega_board.grid[i][j].squares() for i in range(3) for j in range(3)], self.playable_boards, self.winners)
    
    def draw_everything(self):
        self.canvas.create_rectangle(0,0,window_size,window_size,fill=background_color,tag=bg_tag)
        self.draw_big_grid()
        self.draw_boards()
        self.highlight_all_playable_boards()
        
    def draw_big_grid(self):
        for i in [1,2]:
            self.canvas.create_line(i*board_size,pad,i*board_size,window_size-pad,width=5,fill='white')
            self.canvas.create_line(pad,i*board_size,window_size-pad,i*board_size,width=5,fill='white')
        
    def draw_boards(self):
        for b in self.mega_board.squares():
            for i in [1,2]:
                self.canvas.create_line(b.col*board_size+i*sq_size,b.row*board_size+pad,b.col*board_size+i*sq_size,(b.row+1)*board_size-pad,width=5)
                self.canvas.create_line(b.col*board_size+pad,b.row*board_size+i*sq_size,(b.col+1)*board_size-pad,b.row*board_size+i*sq_size,width=5)
            for i in range(3):
                for j in range(3):
                    self.canvas.create_text(b.col*board_size+(2*i+1)*int(sq_size/2),b.row*board_size+(2*j+1)*int(sq_size/2),font=("Purisa", 30),text=b.grid[j][i],fill=piece_color)      
            self.canvas.create_text((2*b.col+1)*int(board_size/2),(2*b.row+1)*int(board_size/2),font=("Purisa", 150),text=b.winner,fill=piece_color)
    
    def highlight_all_playable_boards(self):
        for b in self.playable_boards:
            self.highlight_board(b)
        
    def setup_click(self):
        self.canvas.tag_bind(bg_tag,'<Button-1>', self.respond_to_click)
        
    def setup_undo_button(self):
        frame = tk.Frame()
        frame.pack()
        b = tk.Button(frame,text = "Undo",command = self.undo)
        b.pack()
        
    def undo(self):
        self.state = self.state.prior_state
        self.update_board(self.state.board_config, self.state.winners)
        self.playable_boards = self.state.playable
        self.draw_everything()
        self.change_player()
        
    def update_board(self,board_config,winners):
        board_count = 0
        for b in self.mega_board.squares():
            for i in range(3):
                for j in range(3):
                    b.grid[i][j] = board_config[board_count][3*i+j]
                    b.winner = winners[board_count]
            board_count += 1
        
    def update_state(self):
        self.state = GameState(self.state,[self.mega_board.grid[i][j].squares() for i in range(3) for j in range(3)],self.playable_boards, self.winners)
        
    def respond_to_click(self,event):
        outer_row, outer_col, inner_row, inner_col = self.get_move_coords(event)
        if self.valid_move(outer_row, outer_col, inner_row, inner_col):
            self.do_the_move(outer_row, outer_col, inner_row, inner_col)
            self.reset_counter = True
            
    def do_the_move(self, outer_row, outer_col, inner_row, inner_col):
        self.place_piece(outer_row,outer_col,inner_row,inner_col)
        self.mega_board.grid[outer_row][outer_col].check_win()
        self.update_playable_boards(inner_row,inner_col)
        self.update_winners()
        self.draw_everything()
        self.update_state()
            
    def make_random_coords(self):
        outer_row = random.randint(0,2)
        outer_col = random.randint(0,2)
        inner_row = random.randint(0,2)
        inner_col = random.randint(0,2)
        return outer_row, outer_col, inner_row, inner_col
    
    def make_random_move(self):
        a, b, c, d = self.make_random_coords()
        while not self.valid_move(a, b, c, d):
            a, b, c, d = self.make_random_coords()
        self.do_the_move(a, b, c, d)
            
    def get_move_coords(self,event):
        x, y = event.x, event.y
        outer_row, outer_col = self.which_third(y,board_size), self.which_third(x,board_size)
        inner_row, inner_col = self.which_third(y - outer_row*board_size, sq_size), self.which_third(x - outer_col*board_size, sq_size)
        return outer_row, outer_col, inner_row, inner_col
    
    def valid_move(self,outer_row, outer_col, inner_row, inner_col):
        for b in self.playable_boards:
            if b.row == outer_row and b.col == outer_col and b.grid[inner_row][inner_col] == EMPTY:
                return True
        return False
        
    def which_third(self,a,size):
        if a < size:
            return 0
        elif a < size*2:
            return 1
        else:
            return 2
        
    def place_piece(self,outer_row,outer_col,inner_row,inner_col):
        self.mega_board.grid[outer_row][outer_col].place_piece(self.piece,inner_row,inner_col)
        self.change_player()
            
    def change_player(self):
        if self.piece == X:
            self.piece = O
        else:
            self.piece = X
                
    def update_playable_boards(self,inner_row,inner_col):
        if self.mega_board.grid[inner_row][inner_col].winner == EMPTY_WINNER:
            self.playable_boards = [self.mega_board.grid[inner_row][inner_col]]
        else:
            self.playable_boards = [b for b in self.mega_board.squares() if b.winner == EMPTY_WINNER]
            
    def update_winners(self):
        self.winners = [b.winner for b in self.mega_board.squares()]
        
    def highlight_board(self,b):
        top_left_x , top_left_y = b.col*board_size, b.row*board_size
        bottom_right_x, bottom_right_y = (b.col+1)*board_size, (b.row+1)*board_size
        self.canvas.create_rectangle(top_left_x+pad, top_left_y+pad, bottom_right_x-pad, bottom_right_y-pad,width = 5,outline=board_outline_color)

        
if __name__ == "__main__":
    game = Game()
    game.mainloop()

