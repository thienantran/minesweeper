import sys
import pygame
from pygame.locals import QUIT, MOUSEBUTTONUP
from settings import WINDOW_SIZE, GRID_SIZE
from board import initialize_board, calculate_numbers, draw_board, reveal_cells

def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Minesweeper")

    board, mines = initialize_board()
    calculate_numbers(board)
    revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    flags = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                x, y = event.pos
                row, col = y // GRID_SIZE, x // GRID_SIZE
                if event.button == 1:  # Left-click
                    if not flags[row][col]:  # Make sure you cannot reveal a flagged cell
                        if board[row][col] == "M":
                            print("Game Over!")
                            pygame.quit()
                            sys.exit()
                        else:
                            reveal_cells(row, col, board, revealed)
                elif event.button == 3:  # Right-click
                    flags[row][col] = not flags[row][col]

        screen.fill((255, 255, 255))
        draw_board(board, revealed, flags, screen)
        pygame.display.update()

if __name__ == "__main__":
    main()
