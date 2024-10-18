import pygame
import random
import sys
from enum import Enum
from typing import List, Tuple, Optional
from copy import deepcopy

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 100
GRID_SIZE = 6
WINDOW_SIZE = CELL_SIZE * GRID_SIZE
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Hunt The Wumpus with Alpha Beta Pruning")

# Load images
IMAGES = {
    'gold': pygame.image.load('gold.png'),
    'pit': pygame.image.load('pit.png'),
    'player': pygame.image.load('player.png'),
    'player_armed': pygame.image.load('player-armed.png'),
    'wumpus': pygame.image.load('wumpus.png'),
    'wumpus_dead': pygame.image.load('wumpus_dead.png')
}

# Resize images to fit cells
for key in IMAGES:
    IMAGES[key] = pygame.transform.scale(IMAGES[key], (CELL_SIZE, CELL_SIZE))

class GameState:
    def __init__(self):
        self.grid = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.player_pos = [GRID_SIZE-1, 0]  # Start at bottom left
        self.start_pos = [GRID_SIZE-1, 0]  # Remember the starting position
        self.score = 0
        self.game_over = False
        self.won = False
        self.wumpus_position = None
        self.wumpus_killed = False
        self.gold_collected = False
        self.player_armed = False  # New flag to track if player is armed
        self.visited = set()
        self.visited.add(tuple(self.player_pos))
        self.initialize_grid()

    def initialize_grid(self):
        # Place 1 Wumpus (not near starting position)
        wx, wy = self.random_empty_position(avoid_start=True)
        self.grid[wx][wy] = 'W'
        self.wumpus_position = (wx, wy)
        
        # Place 1 Gold piece (not near starting position)
        gx, gy = self.random_empty_position(avoid_start=True)
        self.grid[gx][gy] = 'G'
        
        # Place Pits (not near starting position)
        for _ in range(2):
            px, py = self.random_empty_position(avoid_start=True)
            self.grid[px][py] = 'P'
        
        # Add breeze and stench
        self.update_percepts()

    def random_empty_position(self, avoid_start=False) -> Tuple[int, int]:
        while True:
            x = random.randint(0, GRID_SIZE-1)
            y = random.randint(0, GRID_SIZE-1)
            if self.grid[x][y] == ' ':
                if not avoid_start or (abs(x - (GRID_SIZE-1)) + abs(y - 0)) > 2:
                    return x, y

    def update_percepts(self):
        # Clear previous percepts
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] in ['B', 'S']:
                    self.grid[i][j] = ' '

        # Add new percepts
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] in ['W', 'P']:
                    for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                            if self.grid[ni][nj] == ' ':
                                if self.grid[i][j] == 'W':
                                    self.grid[ni][nj] = 'S'  # Stench
                                elif self.grid[i][j] == 'P':
                                    self.grid[ni][nj] = 'B'  # Breeze

def evaluate_state(state: GameState, depth: int) -> int:
    if state.game_over:
        if state.won:
            return 10000 + depth  # Prefer winning sooner
        return -10000 - depth  # Prefer losing later
    
    # Base score is current game score
    score = state.score
    
    # Reward exploring new cells
    score += len(state.visited) * 50
    
    # Penalty for revisiting cells
    x, y = state.player_pos
    if tuple(state.player_pos) in state.visited:
        score -= 30
    
    # Bonus for progressing through objectives
    if not state.wumpus_killed:
        # Prioritize finding the Wumpus
        if state.wumpus_position:
            wx, wy = state.wumpus_position
            distance_to_wumpus = abs(x - wx) + abs(y - wy)
            score += (GRID_SIZE * 2 - distance_to_wumpus) * 30
    elif not state.gold_collected:
        # After killing Wumpus, prioritize finding gold
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if state.grid[i][j] == 'G':
                    distance_to_gold = abs(x - i) + abs(y - j)
                    score += (GRID_SIZE * 2 - distance_to_gold) * 40
                    break
    else:
        # After collecting gold, prioritize returning to start
        distance_to_start = abs(x - state.start_pos[0]) + abs(y - state.start_pos[1])
        score += (GRID_SIZE * 2 - distance_to_start) * 50

    return score

def get_valid_moves(state: GameState) -> List[Tuple[int, int]]:
    x, y = state.player_pos
    moves = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            moves.append((new_x, new_y))
    return moves

def alpha_beta_pruning(state: GameState, depth: int, alpha: float, beta: float, maximizing: bool) -> Tuple[int, Optional[Tuple[int, int]]]:
    if depth == 0 or state.game_over:
        return evaluate_state(state, depth), None

    valid_moves = get_valid_moves(state)
    
    if maximizing:
        max_eval = float('-inf')
        best_move = None
        for move in valid_moves:
            new_state = deepcopy(state)
            new_state.player_pos = list(move)
            new_state.score -= 1  # Cost for moving
            new_state.visited.add(tuple(move))
            
            # Check what's in the new position
            x, y = move
            if new_state.grid[x][y] == 'W' and not new_state.wumpus_killed:
                new_state.score += 500
                new_state.wumpus_killed = True
                new_state.player_armed = True  # Player becomes armed after killing Wumpus
                new_state.grid[x][y] = ' '  # Remove Wumpus from the grid
            elif new_state.grid[x][y] == 'G' and not new_state.gold_collected:
                new_state.score += 1000
                new_state.gold_collected = True
                new_state.player_armed = False  # Player becomes unarmed after collecting Gold
                new_state.grid[x][y] = ' '  # Remove Gold from the grid
            elif new_state.grid[x][y] == 'P':
                new_state.score -= 1000
                new_state.game_over = True
                new_state.won = False
            
            # Check win condition
            if new_state.wumpus_killed and new_state.gold_collected and new_state.player_pos == new_state.start_pos:
                new_state.game_over = True
                new_state.won = True
                new_state.score += 2000  # Bonus for completing all objectives
            
            eval_score, _ = alpha_beta_pruning(new_state, depth - 1, alpha, beta, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in valid_moves:
            new_state = deepcopy(state)
            new_state.player_pos = list(move)
            new_state.score -= 1
            new_state.visited.add(tuple(move))
            
            eval_score, _ = alpha_beta_pruning(new_state, depth - 1, alpha, beta, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

def main():
    clock = pygame.time.Clock()
    game_state = GameState()
    running = True
    move_delay = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_state.game_over:
            move_delay += 1
            if move_delay >= 10:  # Add delay between moves
                move_delay = 0
                # AI move using Alpha-Beta Pruning
                _, best_move = alpha_beta_pruning(game_state, 5, float('-inf'), float('inf'), True)
                if best_move:
                    x, y = best_move
                    game_state.player_pos = [x, y]
                    game_state.visited.add((x, y))
                    game_state.score -= 1
                    
                    # Check for Wumpus
                    if game_state.grid[x][y] == 'W' and not game_state.wumpus_killed:
                        game_state.score += 500
                        game_state.wumpus_killed = True
                        game_state.player_armed = True  # Player becomes armed after killing Wumpus
                        game_state.grid[x][y] = ' '  # Remove Wumpus from the grid
                    
                    # Check for Gold
                    elif game_state.grid[x][y] == 'G' and not game_state.gold_collected:
                        game_state.score += 1000
                        game_state.gold_collected = True
                        game_state.player_armed = False  # Player becomes unarmed after collecting Gold
                        game_state.grid[x][y] = ' '  # Remove Gold from the grid
                    
                    # Check for Pit
                    elif game_state.grid[x][y] == 'P':
                        game_state.score -= 1000
                        game_state.game_over = True
                        game_state.won = False
                    
                    # Check win condition
                    if game_state.wumpus_killed and game_state.gold_collected and game_state.player_pos == game_state.start_pos:
                        game_state.game_over = True
                        game_state.won = True
                        game_state.score += 2000  # Bonus for completing all objectives

        # Draw game state
        screen.fill((255, 255, 255))
        
        # Draw grid
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                pygame.draw.rect(screen, (0, 0, 0), 
                               (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
                
                # Draw visited cells with light gray background
                if (i, j) in game_state.visited:
                    pygame.draw.rect(screen, (240, 240, 240),
                                   (j * CELL_SIZE + 1, i * CELL_SIZE + 1, 
                                    CELL_SIZE - 2, CELL_SIZE - 2))
                
                cell = game_state.grid[i][j]
                if cell == 'W':
                    screen.blit(IMAGES['wumpus'], (j * CELL_SIZE, i * CELL_SIZE))
                elif cell == 'G':
                    screen.blit(IMAGES['gold'], (j * CELL_SIZE, i * CELL_SIZE))
                elif cell == 'P':
                    screen.blit(IMAGES['pit'], (j * CELL_SIZE, i * CELL_SIZE))
                elif cell in ['B', 'S']:
                    font = pygame.font.Font(None, 36)
                    text = font.render(cell, True, (0, 0, 0))
                    screen.blit(text, (j * CELL_SIZE + 40, i * CELL_SIZE + 40))

        # Draw player
        px, py = game_state.player_pos
        if game_state.player_armed:
            screen.blit(IMAGES['player_armed'], (py * CELL_SIZE, px * CELL_SIZE))
        else:
            screen.blit(IMAGES['player'], (py * CELL_SIZE, px * CELL_SIZE))

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {game_state.score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Display game status
        font = pygame.font.Font(None, 24)
        status_text = f"Wumpus Killed: {'Yes' if game_state.wumpus_killed else 'No'}"
        status_text += f" | Gold Collected: {'Yes' if game_state.gold_collected else 'No'}"
        status = font.render(status_text, True, (0, 0, 0))
        screen.blit(status, (10, WINDOW_SIZE - 30))

        # Display game over message
        if game_state.game_over:
            message = "You Won!" if game_state.won else "Game Over!"
            text = font.render(message, True, (0, 255, 0) if game_state.won else (255, 0, 0))
            screen.blit(text, (WINDOW_SIZE // 2 - 100, WINDOW_SIZE // 2))

        pygame.display.flip()
        clock.tick(30)  # Higher FPS for smoother animation

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()