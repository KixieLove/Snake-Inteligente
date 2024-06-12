import numpy as np
from collections import deque
import random
import os
import time
import math

SQUARE = 255
# Mejores movimientos predefinidos para el juego automático
BEST_MOVES = [2, 3, 3, 2, 2, 4, 4, 4, 2, 4, 4, 1, 3, 3, 1, 1, 1, 4, 4, 1, 1, 1, 4, 4, 4, 1, 4, 1, 1, 1, 3, 2, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 2, 3, 3, 2, 2, 3, 1, 1, 1, 2, 1, 2, 4, 3, 1, 1, 4, 1, 1, 1, 4, 4, 1, 4, 3, 2, 1, 4, 4, 1, 2, 4, 4, 2, 4, 4, 1, 3, 3, 2, 3, 4, 2, 2, 1, 2, 2, 1, 2, 1, 3, 4, 2, 1, 4, 4]
BOARD_SIZE = 20
# Direcciones posibles: 1: Arriba, 2: Abajo, 3: Izquierda, 4: Derecha
DIRECTIONS = [1, 2, 3, 4]
# Mapeo de direcciones a cambios de coordenadas
DIRECTION_MAP = {
    1: (-1, 0),  # Arriba
    2: (1, 0),   # Abajo
    3: (0, -1),  # Izquierda
    4: (0, 1)    # Derecha
}

# Inicializa el juego creando el tablero, la serpiente y las frutas
def initialize_game():
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    snake = deque([(BOARD_SIZE//2, BOARD_SIZE//2)])
    fruits = [(5, 6), (7, 16), (13, 8), (14, 13), (3, 17)]
    for fruit in fruits:
        board[fruit] = 1  # 1 representa una fruta
    return board, snake, fruits

from colorama import Fore, Back, Style

# Imprime el estado actual del juego
def print_game_state(board, snake):
    temp_board = np.copy(board)
    for x, y in snake:
        temp_board[x, y] = 2  # 2 representa la serpiente
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if temp_board[i, j] == 0:
                print(' . ', end='')  # Espacio vacío
            elif temp_board[i, j] == 1:
                print(Fore.RED + ' ' + chr(9724) + ' ' + Style.RESET_ALL, end='')  # Fruta roja
            else:
                print(Fore.GREEN + ' ' + chr(9724) + ' ' + Style.RESET_ALL, end='')  # Serpiente verde
        print()
    print()

# Puntuación inicial
score = 0

# Aplica un movimiento a la serpiente y actualiza el tablero, la serpiente y las frutas
def apply_move(move, board, snake, fruits, individual=None, index=None):
    global score
    dx, dy = DIRECTION_MAP[move]
    head_x, head_y = snake[0]
    new_head = (head_x + dx, head_y + dy)
    if (new_head[0] < 0 or new_head[0] >= BOARD_SIZE or 
        new_head[1] < 0 or new_head[1] >= BOARD_SIZE or 
        new_head in snake):
        return False  # Fin del juego
    snake.appendleft(new_head)
    if new_head in fruits:
        fruits.remove(new_head)
        score += 5  # Aumenta la puntuación cuando la serpiente come una fruta
        if individual and index is not None:  # Comprueba si se proporcionan individual e index
            score += math.exp(math.exp((len(individual) - index) / len(individual)))  # Puntuación adicional
    else:
        snake.pop()
    return True

# Permite al usuario jugar el juego manualmente
def play_game_manually():
    global score
    board, snake, fruits = initialize_game()
    move_count = 0  # Inicializa el contador de movimientos
    move_map = {'w': 1, 's': 2, 'a': 3, 'd': 4}  # Mapea 'w', 'a', 's', 'd' a 1, 2, 3, 4
    while True:
        print_game_state(board, snake)
        move = input("Introduce el movimiento (w: Arriba, s: Abajo, a: Izquierda, d: Derecha): ")
        if move not in move_map:
            print("¡Movimiento inválido! Por favor, introduce 'w', 'a', 's' o 'd'.")
            continue
        if not apply_move(move_map[move], board, snake, fruits, [0]*100, move_count) or is_game_over(snake):
            print("¡Fin del juego! Tu puntuación es: ", score)
            break
        print("Puntuación actual: ", score)  # Imprime la puntuación actual después de cada movimiento
        move_count += 1  # Incrementa el contador de movimientos

# Juega el juego automáticamente usando los movimientos predefinidos
def play_game_automatically(moves):
    global score
    board, snake, fruits = initialize_game()
    for index, move in enumerate(moves):
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpia la consola
        print_game_state(board, snake)
        if not apply_move(move, board, snake, fruits, moves, index) or is_game_over(snake):
            print("¡Fin del juego! Tu puntuación es: ", score)
            break
        print("Puntuación actual: ", score)  # Imprime la puntuación actual después de cada movimiento
        time.sleep(0.1)  # Retraso de 0.1 segundos

# Comprueba si el juego ha terminado
def is_game_over(snake):
    head_x, head_y = snake[0]
    return (head_x < 0 or head_x >= BOARD_SIZE or 
            head_y < 0 or head_y >= BOARD_SIZE or 
            snake.count(snake[0]) > 1)

print("Elige el modo: 1. Manual, 2. Automático")
mode = int(input())
if mode == 1:
    play_game_manually()
else: 
    moves = BEST_MOVES
    play_game_automatically(moves)

# BEST_MOVES = [2, 3, 3, 2, 2, 4, 4, 4, 2, 4, 4, 1, 3, 3, 1, 1, 1, 4, 4, 1, 1, 1, 4, 4, 4, 1, 4, 1, 1, 1, 3, 2, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 2, 3, 3, 2, 2, 3, 1, 1, 1, 2, 1, 2, 4, 3, 1, 1, 4, 1, 1, 1, 4, 4, 1, 4, 3, 2, 1, 4, 4, 1, 2, 4, 4, 2, 4, 4, 1, 3, 3, 2, 3, 4, 2, 2, 1, 2, 2, 1, 2, 1, 3, 4, 2, 1, 4, 4]
# BOARD_SIZE = 20