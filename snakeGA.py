import numpy as np
from collections import deque
import random
import math
import pickle
import matplotlib.pyplot as plt
import json
import os

BOARD_SIZE = 20

board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

snake = deque([(BOARD_SIZE // 2, BOARD_SIZE // 2)])

fruits = [(5, 6), (7, 16), (13, 8), (14, 13), (3, 17)]

for fruit in fruits:
    board[fruit] = 1  # 1 representa una fruta

# Función para imprimir el tablero
def print_board(board, snake):
    temp_board = np.copy(board)
    for x, y in snake:
        temp_board[x, y] = 2  # 2 representa la snake
    print(temp_board)

# Mostramos el tablero inicial
print_board(board, snake)

# Parámetros del algoritmo genético
POPULATION_SIZE = 1000
SNAKE_LENGTH = 100 
MUTATION_RATE = 0.001
NUM_GENERATIONS = 5000

# Direcciones posibles (1: Arriba, 2: Abajo, 3: Izquierda, 4: Derecha)
DIRECTIONS = [1, 2, 3, 4]

# Función para crear un individuo
def create_individual():
    return [random.choice(DIRECTIONS) for _ in range(SNAKE_LENGTH)]

# Función para crear la población inicial
def create_population(size):
    return [create_individual() for _ in range(size)]

# Función de evaluación
def evaluate_individual(individual, board, snake, fruits):

    snake_copy = deque(snake)
    score = 0
    moves = 0
    fruits_eaten = 0
    crash_penalty = 0

    # Mapeo de direcciones a movimientos en el tablero
    direction_map = {
        1: (-1, 0),  # Arriba
        2: (1, 0),   # Abajo
        3: (0, -1),  # Izquierda
        4: (0, 1)    # Derecha
    }

    fruits_copy = fruits[:]

    fruit_eating_moves = []
    
    for index, move in enumerate(individual):
        dx, dy = direction_map[move]
        head_x, head_y = snake_copy[0]
        new_head = (head_x + dx, head_y + dy)

        # Verificamos colisiones con las paredes o el cuerpo de la snake
        if (new_head[0] < 0 or new_head[0] >= BOARD_SIZE or 
            new_head[1] < 0 or new_head[1] >= BOARD_SIZE or 
            new_head in snake_copy):
            crash_penalty = -100
            break
        
        # Movemos la snake
        snake_copy.appendleft(new_head)
        if new_head in fruits_copy:
            score += 5
            fruits_copy.remove(new_head)
            fruits_eaten += 1
            fruit_eating_moves.append((index, move, new_head))
            score += math.exp(math.exp((len(individual) - index) / len(individual)))
            if len(fruits_copy) == 0:  # Ya no hay frutas
                break
        else:
            snake_copy.pop()

        moves += 1

    # Penalización por movimientos innecesarios
    penalty = moves / SNAKE_LENGTH

    return score + crash_penalty, fruits_eaten, fruit_eating_moves

# Función para seleccionar a los padres usando torneo
def tournament_selection(population, scores, k=3):
    selected = random.sample(list(zip(population, scores)), k)
    selected = sorted(selected, key=lambda x: x[1], reverse=True)
    return selected[0][0]

# Función para cruzar dos individuos
def crossover(parent1, parent2):
    point1 = random.randint(1, SNAKE_LENGTH - 2)
    point2 = random.randint(point1, SNAKE_LENGTH - 1)
    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    return child1, child2

# Función para mutar un individuo
def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.choice(DIRECTIONS)
    return individual

# Crear la población inicial
population = create_population(POPULATION_SIZE)

all_generations = []

best_fruits_eaten = 0
best_score = float('-inf')
best_individual = None
best_scores = []
avg_scores = []

# Evolucionar la población
for generation in range(NUM_GENERATIONS):
    # Evaluar la población
    results = [evaluate_individual(ind, np.copy(board), deque(snake), fruits[:]) for ind in population]
    scores, fruits_eaten, fruit_eating_moves = zip(*results)

    best_scores.append(max(scores))
    avg_scores.append(sum(scores) / len(scores))
    
    # Checar si el mejor individuo de la generación actual es mejor que el mejor individuo global
    max_index = scores.index(max(scores))
    if fruits_eaten[max_index] > best_fruits_eaten:
        best_fruits_eaten = fruits_eaten[max_index]

    all_generations.append(population[:])

    # Seleccionar los mejores individuos
    next_population = []
    for _ in range(POPULATION_SIZE // 2):
        parent1 = tournament_selection(population, scores)
        parent2 = tournament_selection(population, scores)
        child1, child2 = crossover(parent1, parent2)
        next_population.append(mutate(child1, MUTATION_RATE))
        next_population.append(mutate(child2, MUTATION_RATE))
    


    # Imprimir la mejor puntuación de cada generación
    current_best_score = max(scores)
    print(f"Generación {generation}: Mejor puntuación = {current_best_score}")

    if current_best_score > best_score:
        best_score = current_best_score
        best_individual = population[scores.index(current_best_score)]
    
    population = next_population

# Evaluar el mejor individuo

results = evaluate_individual(best_individual, np.copy(board), deque(snake), fruits[:])
best_score, best_fruits_eaten, best_fruit_eating_moves = results
print(f"Mejor secuencia de movimientos: {best_individual}")
print(f"Número de frutas comidas por el mejor individuo: {best_fruits_eaten}")
print(f"Puntuación del mejor individuo: {best_score}")
print(f"Movimientos que resultaron en comer una fruta (index, movimiento, (posición de la fruta)): {best_fruit_eating_moves}")


directory = r'D:\UAEM\4to semestre\Busqueda bayesiana\Codes'
os.makedirs(directory, exist_ok=True)
file_path = os.path.join(directory, 'data.pkl')

data = {
    'all_generations': all_generations,
    'best_individual': list(best_individual),
    'best_scores': best_scores,
    'avg_scores': avg_scores,
    'best_score': best_score,
    'best_fruits_eaten': best_fruits_eaten,
    'results': (results[0], results[1], [(index, move, list(pos)) for index, move, pos in results[2]]),
    'scores': list(scores)
}

with open(file_path, 'wb') as f:
    pickle.dump(data, f)
