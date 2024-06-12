import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pickle
from matplotlib.patches import Rectangle

# Cargar los datos
with open('data.pkl', 'rb') as f:
    data = pickle.load(f)

all_generations = data['all_generations']
fruits = [(5, 6), (7, 16), (13, 8), (14, 13), (3, 17)]
BOARD_SIZE = 20
FRUIT_VALUE = -3

# Añadir un diccionario para llevar un registro de las frutas comidas por cada serpiente
eaten_fruits = {i: set() for i in range(len(all_generations[0]))}

def draw_board(board, generation, move):
    # Limpiar el tablero
    board.fill(0)
    # Actualizar el tablero con las nuevas posiciones de las serpientes
    for i, snake in enumerate(all_generations[generation]):
        # Iniciar la serpiente desde una posición fija
        x, y = 10, 10
        visited = set()  # Posiciones que esta serpiente ha visitado
        alive = True  # Si esta serpiente está viva
        for direction in snake[:move]:
            # Actualizar la posición de acuerdo a la dirección
            if direction == 1:  # Arriba
                x -= 1
            elif direction == 2:  # Derecha
                y += 1
            elif direction == 3:  # Abajo
                x += 1
            elif direction == 4:  # Izquierda
                y -= 1
            # Verificar colisiones con el borde del tablero
            if x < 0 or x >= BOARD_SIZE or y < 0 or y >= BOARD_SIZE:
                alive = False  # La serpiente "muere"
                break
            # Verificar colisiones consigo misma
            if (x, y) in visited:
                alive = False  # La serpiente "muere"
                break
            # Verificar frutas
            if (x, y) in fruits:
                if (x, y) not in eaten_fruits[i]:
                    eaten_fruits[i].add((x, y))  # La fruta es comida
                    visited.add((x, y))  # La serpiente crece
            else:
                if visited:
                    visited.pop()  # La serpiente se mueve
                visited.add((x, y))
        # Dibujar la serpiente en el tablero
        for position in visited:
            # Solo dibujar la serpiente si la posición no contiene una fruta
            if board[position] != -1:
                board[position] = -2 if not alive else i + 1  # -2 representa una serpiente muerta, i+1 representa una serpiente viva
    
    # Crear un tablero separado para las frutas
    fruit_board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    # Dibujar las frutas en el tablero de frutas
    for fruit in fruits:
        if all(fruit not in eaten for eaten in eaten_fruits.values()):
            fruit_board[fruit] = FRUIT_VALUE  # FRUIT_VALUE representa una fruta
    
    # Fusionar el tablero de serpientes y el tablero de frutas
    board += fruit_board
    
    return board

# Crear una figura y un eje para la animación
fig, ax = plt.subplots()

# Definir el tablero
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

# Función de actualización para la animación
def update(frame, generation, board):
    ax.clear()
    move = frame
    draw_board(board, generation, move)  # Actualizar el tablero existente en su lugar
    ax.imshow(board, cmap='Accent')
    ax.set_title(f"Generación {generation}, Movimiento {move}")

    # Añadir los cuadrados
    squares = [(5, 6), (7, 16), (13, 8), (14, 13), (3, 17)]
    for square in squares:
        rect = Rectangle((square[1], square[0]), 1, 1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

# Especificar la generación que quieres visualizar
generation_to_visualize = 500

# Crear la animación para la generación especificada
ani = animation.FuncAnimation(fig, update, frames=100, fargs=(generation_to_visualize, board))

# Mostrar la animación
plt.show()
