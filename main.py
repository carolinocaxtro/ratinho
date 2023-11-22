import pygame
import sys
from collections import deque

# Tamanho da janela
WIDTH, HEIGHT = 400, 400

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Inicialização do Pygame
pygame.init()
pygame.display.set_caption("Rat in a Maze")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Lógica para ler o labirinto a partir de um arquivo
def read_maze(file_name):
    with open(file_name, 'r') as file:
        maze = [list(line.strip()) for line in file.readlines()]
    return maze

# Encontrar a posição inicial do rato (ponto vermelho) e do queijo (ponto azul)
def find_positions(maze):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 'e':
                rat_pos = (x, y)
            elif maze[y][x] == 'm':
                cheese_pos = (x, y)
    return rat_pos, cheese_pos

# Desenhar o labirinto
def draw_maze(maze):
    cell_width = WIDTH / len(maze[0])
    cell_height = HEIGHT / len(maze)

    for y in range(len(maze)):
        for x in range(len(maze[0])):
            color = WHITE if maze[y][x] == '1' else BLACK
            pygame.draw.rect(screen, color, (x * cell_width, y * cell_height, cell_width, cell_height))

            if maze[y][x] == 'e':
                pygame.draw.rect(screen, RED, (x * cell_width, y * cell_height, cell_width, cell_height))
            elif maze[y][x] == 'm':
                pygame.draw.rect(screen, BLUE, (x * cell_width, y * cell_height, cell_width, cell_height))

    pygame.display.flip()

# Encontra o caminho no labirinto utilizando pilhas
def solve_maze(maze, start, end):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    stack = deque()
    stack.append(start)
    visited = set()

    while stack:
        x, y = stack.pop()
        if (x, y) == end:
            return True

        if (x, y) not in visited:
            visited.add((x, y))
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze) and maze[new_y][new_x] != '1':
                    stack.append((new_x, new_y))
                    maze[new_y][new_x] = '.'
                    pygame.draw.rect(screen, GREEN, (new_x * (WIDTH / len(maze[0])), new_y * (HEIGHT / len(maze)), WIDTH / len(maze[0]), HEIGHT / len(maze)))
                    pygame.display.flip()
                    clock.tick(10)
    return False

# Carrega o labirinto do arquivo 'labirinto2.txt'
maze = read_maze('labirinto2.txt')

# Desenha o labirinto inicial
draw_maze(maze)

# Encontra as posições iniciais do rato e do queijo
rat_pos, cheese_pos = find_positions(maze)

# Resolução do labirinto
if solve_maze(maze, rat_pos, cheese_pos):
    print("Caminho encontrado!")
else:
    print("Caminho não encontrado!")

# Loop principal do Pygame
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(5)

pygame.quit()
sys.exit()



