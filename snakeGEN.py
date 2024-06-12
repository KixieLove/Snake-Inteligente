import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pickle
from matplotlib.patches import Rectangle

# Load the data
with open('data.pkl', 'rb') as f:
    data = pickle.load(f)

all_generations = data['all_generations']
fruits = [(5, 6), (7, 16), (13, 8), (14, 13), (3, 17)]
BOARD_SIZE = 20
FRUIT_VALUE = -3

# Add a dictionary to keep track of fruits eaten by each snake
eaten_fruits = {i: set() for i in range(len(all_generations[0]))}

def draw_board(board, generation, move):
    # Clear the board
    board.fill(0)
    # Update the board with the new positions of the snakes
    for i, snake in enumerate(all_generations[generation]):
        # Start the snake from a fixed position
        x, y = 10, 10
        visited = set()  # Positions that this snake has visited
        alive = True  # Whether this snake is alive
        for direction in snake[:move]:
            # Update the position according to the direction
            if direction == 1:  # Up
                x -= 1
            elif direction == 2:  # Right
                y += 1
            elif direction == 3:  # Down
                x += 1
            elif direction == 4:  # Left
                y -= 1
            # Check for collisions with the edge of the board
            if x < 0 or x >= BOARD_SIZE or y < 0 or y >= BOARD_SIZE:
                alive = False  # The snake "dies"
                break
            # Check for collisions with self
            if (x, y) in visited:
                alive = False  # The snake "dies"
                break
            # Check for fruits
            if (x, y) in fruits:
                if (x, y) not in eaten_fruits[i]:
                    eaten_fruits[i].add((x, y))  # The fruit is eaten
                    visited.add((x, y))  # The snake grows
            else:
                if visited:
                    visited.pop()  # The snake moves
                visited.add((x, y))
        # Draw the snake on the board
        for position in visited:
            # Only draw the snake if the position does not contain a fruit
            if board[position] != -1:
                board[position] = -2 if not alive else i + 1  # -2 represents a dead snake, i+1 represents a live snake
    
    # Create a separate board for fruits
    fruit_board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    # Draw the fruits on the fruit board
    for fruit in fruits:
        if all(fruit not in eaten for eaten in eaten_fruits.values()):
            fruit_board[fruit] = FRUIT_VALUE  # FRUIT_VALUE represents a fruit
    
    # Merge the snake board and fruit board
    board += fruit_board
    
    return board

# Create a figure and axis for the animation
fig, ax = plt.subplots()

# Define the board
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

# Update function for the animation
def update(frame, generation, board):
    ax.clear()
    move = frame
    draw_board(board, generation, move)  # Update the existing board in-place
    ax.imshow(board, cmap='Accent')
    ax.set_title(f"Generation {generation}, Move {move}")

    # Add the squares
    squares = [(5, 6), (7, 16), (13, 8), (14, 13), (3, 17)]
    for square in squares:
        rect = Rectangle((square[1], square[0]), 1, 1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

# Specify the generation you want to visualize
generation_to_visualize = 500

# Create the animation for the specified generation
ani = animation.FuncAnimation(fig, update, frames=100, fargs=(generation_to_visualize, board))

# Display the animation
plt.show()
