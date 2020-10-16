import tkinter as tk
import random
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
X = 'X'
O = 'O'
EMPTY = ''
EMPTY_WINNER = ''
BOARD = 'board'


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
    
    
class GameState:
    
    def __init__(self, prior_state, board_config, playable, winners):
        self.prior_state = prior_state
        self.board_config = board_config
        self.playable = playable
        self.winners = winners
    
    
class Game(tk.Tk):
    
    def __init__(self):
        self.setup_game()
        self.setup_canvas()
        self.setup_click()
        self.setup_pause_button()
        self.setup_undo_button()
        
    def setup_canvas(self):
        tk.Tk.__init__(self)
        self.setup_timer()
        self.setup_names()
        self.canvas = tk.Canvas(height=window_size,width=window_size)
        self.canvas.pack()
        self.draw_everything()

    def setup_names(self):
        self.name_label = tk.Label(font=("Helvetica", 36))
        self.name_label['text'] = self.piece + "'s move"
        self.name_label.place(x=1100,y=5)
        
    def setup_timer(self):
        self.time_label = tk.Label(font=("Helvetica", 36))
        self.time_label.place(x=5,y=5)
        self.reset_counter = False
        self.paused = True
        self.count = 10
        self.countdown()
        
    def countdown(self):
        if self.count >= 0 and not self.reset_counter:
            self.time_label['text'] = str(round(self.count,2))
            if not self.paused:
                self.count -= 1
                self.after(duration,self.countdown)
        else:
            if not self.reset_counter:
                self.make_random_move()
            self.reset_counter = False
            self.count = 10
            self.time_label['text'] = str(round(self.count,2))
            if not self.paused:
                self.count -= 1
                self.after(duration,self.countdown) 
        
    def setup_game(self):
        self.mega_board = TicTacToeBoard(BOARD,None,None,)
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
        
    def setup_pause_button(self):
        frame = tk.Frame()
        frame.pack()
        self.pause_button = tk.Button(frame,text = "Start Timer", font=("Helvetica", 16), command = self.pause)
        self.pause_button.pack()
        
    def pause(self):
        if not self.paused:
            self.paused = True
            self.pause_button['text'] = "Resume Timer"
        else:
            self.paused = False
            self.pause_button['text'] = "Pause Timer"
            self.after(100,self.countdown)
        
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
        self.name_label['text'] = self.piece + "'s move"
                
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
        
class GetNames(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.e1 = tk.Entry()
        self.e1.pack()
        l1 = tk.Label(text = "X team")
        l1.pack()
        l2 = tk.Label(text = "O team")
        l2.pack()
        self.e2 = tk.Entry()
        self.e2.pack()
        b = tk.Button(text="Start game", width=50, command=self.save_names)
        b.pack()
        
    def save_names(self):
        self.x_team = self.e1.get()
        self.o_team = self.e2.get()
        self.destroy()
        
if __name__ == "__main__":
    # g = GetNames()
    # g.mainloop()
    # game = Game(g.x_team,g.o_team)
    game = Game()
    game.mainloop()
