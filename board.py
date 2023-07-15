import random
import pygame
from settings import GRID_WIDTH, GRID_HEIGHT, MINE_COUNT, GRID_SIZE


def initialize_board():
    board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    mines = set()
    while len(mines) < MINE_COUNT:
        row = random.randint(0, GRID_HEIGHT - 1)
        col = random.randint(0, GRID_WIDTH - 1)
        if (row, col) not in mines:
            mines.add((row, col))
            board[row][col] = "M"
    return board, mines

def calculate_numbers(board):
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if board[row][col] == "M":
                continue
            count = 0
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < GRID_HEIGHT and 0 <= c < GRID_WIDTH and board[r][c] == "M":
                        count += 1
            board[row][col] = count

def draw_board(board, revealed, flags, screen):
    number_colors = {
        1: (0, 0, 255),
        2: (0, 128, 0),
        3: (255, 0, 0),
        4: (0, 0, 128),
        5: (128, 0, 0),
        6: (0, 128, 128),
        7: (0, 0, 0),
        8: (128, 128, 128),
    }

    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if revealed[row][col]:
                color = (200, 200, 200)
            else:
                color = (100, 100, 100)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Draw cell border

            if revealed[row][col] and board[row][col] != 0:
                if board[row][col] == "M":
                    font = pygame.font.Font(None, 36)
                    text = font.render("M", True, (0, 0, 0))
                    screen.blit(text, rect.move(6, 3))
                else:
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(board[row][col]), True, number_colors.get(board[row][col], (0, 0, 0)))
                    screen.blit(text, rect.move(6, 3))

            if flags[row][col]:
                font = pygame.font.Font(None, 36)
                text = font.render("F", True, (0, 0, 0))
                screen.blit(text, rect.move(6, 3))

def reveal_cells(row, col, board, revealed):
    if not (0 <= row < GRID_HEIGHT) or not (0 <= col < GRID_WIDTH) or revealed[row][col]:
        return

    revealed[row][col] = True

    if board[row][col] > 0:
        return
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            reveal_cells(r, c, board, revealed)

    def toggle_flag(row, col, flags):
        flags[row][col] = not flags[row][col]
