import tkinter as tk
from tkinter import messagebox

# Game Layout Constants
GRID_SIZE = 40
GRID_WIDTH = 15
GRID_HEIGHT = 15

# Colors (Hex format for Tkinter rendering)
BG_COLOR = "#1e1e1e"        # Dark background
WALL_COLOR = "#505050"      # Gray obstacles
PLAYER_COLOR = "#00ff64"    # Green Player (You)
GHOST_COLOR = "#ff3232"     # Red Ghost (Greedy AI)
EXIT_COLOR = "#ffd700"      # Gold Escape Portal
LINE_COLOR = "#2d2d2d"      # Subtle grid lines

# Flat layout matrix to completely prevent formatting syntax errors
MAZE_STRING = (
    "111111111111111"
    "100001000000001"
    "101101011111011"
    "101000000010001"
    "101111101011101"
    "100000101000101"
    "111101101110101"
    "100001000010001"
    "101111011011111"
    "101000010000001"
    "101011111111011"
    "100010000010001"
    "111010111010101"
    "100000010000101"
    "111111111111111"
)

# Convert flat layout safely into numerical indices
MAZE = []
for i in range(GRID_HEIGHT):
    row_str = MAZE_STRING[i*GRID_WIDTH : (i+1)*GRID_WIDTH]
    row_nums = [int(char) for char in row_str]
    MAZE.append(row_nums)

class GreedyGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Greedy Algorithm Project - Ghost Escape AI")
        
        # Coordinate tracking [Row, Column]
        self.player_pos = [1, 1]
        self.ghost_pos = [13, 1]
        self.exit_pos = [7, 7]
        
        # Setup UI Elements
        self.canvas = tk.Canvas(root, width=GRID_WIDTH*GRID_SIZE, height=GRID_HEIGHT*GRID_SIZE, bg=BG_COLOR)
        self.canvas.pack()
        
        # Bind Movement Events
        self.root.bind("<Up>", lambda e: self.move_player(-1, 0))
        self.root.bind("<Down>", lambda e: self.move_player(1, 0))
        self.root.bind("<Left>", lambda e: self.move_player(0, -1))
        self.root.bind("<Right>", lambda e: self.move_player(0, 1))
        
        self.game_over = False
        self.draw_game()
        self.game_loop()

    def manhattan_distance(self, p1, p2):
        """Heuristic Cost Calculation Function: H(n)"""
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def get_greedy_move(self):
        """THE GREEDY ALGORITHM: Examines immediate moves and picks local minimum distance"""
        possible_moves = [
            [self.ghost_pos[0] + 1, self.ghost_pos[1]],  # Down
            [self.ghost_pos[0] - 1, self.ghost_pos[1]],  # Up
            [self.ghost_pos[0], self.ghost_pos[1] + 1],  # Right
            [self.ghost_pos[0], self.ghost_pos[1] - 1]   # Left
        ]
        
        best_move = self.ghost_pos
        min_distance = float('inf')
        
        for move in possible_moves:
            if 0 <= move[0] < GRID_HEIGHT and 0 <= move[1] < GRID_WIDTH:
                if MAZE[move[0]][move[1]] == 0:
                    distance = self.manhattan_distance(move, self.player_pos)
                    if distance < min_distance:
                        min_distance = distance
                        best_move = move
                        
        return best_move

    def move_player(self, dr, dc):
        if self.game_over: return
        new_r = self.player_pos[0] + dr
        new_c = self.player_pos[1] + dc
        
        if MAZE[new_r][new_c] == 0:
            self.player_pos = [new_r, new_c]
            self.check_game_states()
            self.draw_game()

    def game_loop(self):
        """Triggers Greedy AI loop cycles automatically every 400ms"""
        if not self.game_over:
            self.ghost_pos = self.get_greedy_move()
            self.check_game_states()
            self.draw_game()
            self.root.after(400, self.game_loop)

    def check_game_states(self):
        if self.player_pos == self.ghost_pos:
            self.game_over = True
            messagebox.showinfo("Game Over", "Caught by the Greedy AI Enemy Agent!")
            self.root.destroy()
        elif self.player_pos == self.exit_pos:
            self.game_over = True
            messagebox.showinfo("Victory", "Congratulations! You safely escaped the maze layout.")
            self.root.destroy()

    def draw_game(self):
        self.canvas.delete("all")
        
        # Draw Grids & Walls
        for r in range(GRID_HEIGHT):
            for c in range(GRID_WIDTH):
                x1, y1 = c * GRID_SIZE, r * GRID_SIZE
                x2, y2 = x1 + GRID_SIZE, y1 + GRID_SIZE
                
                if MAZE[r][c] == 1:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=WALL_COLOR, outline=LINE_COLOR)
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=BG_COLOR, outline=LINE_COLOR)
                    
        # Draw Exit Point
        ex1, ey1 = self.exit_pos[1]*GRID_SIZE, self.exit_pos[0]*GRID_SIZE
        self.canvas.create_rectangle(ex1+4, ey1+4, ex1+GRID_SIZE-4, ey1+GRID_SIZE-4, fill=EXIT_COLOR, outline="")
        
        # Draw Player Object
        px1, py1 = self.player_pos[1]*GRID_SIZE, self.player_pos[0]*GRID_SIZE
        self.canvas.create_oval(px1+6, py1+6, px1+GRID_SIZE-6, py1+GRID_SIZE-6, fill=PLAYER_COLOR, outline="")
        
        # Draw Greedy Enemy Object
        gx1, gy1 = self.ghost_pos[1]*GRID_SIZE, self.ghost_pos[0]*GRID_SIZE
        self.canvas.create_oval(gx1+6, gy1+6, gx1+GRID_SIZE-6, gy1+GRID_SIZE-6, fill=GHOST_COLOR, outline="")

if __name__ == "__main__":
    root = tk.Tk()
    game = GreedyGame(root)
    root.mainloop()
