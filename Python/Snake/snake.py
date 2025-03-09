from turtle import *
from gamebase import square
from random import randrange
from time import sleep
import time

# Initialize the snake's position, represented as a list of coordinates of each part of the snake's body
snake = [[0, 0], [10, 0], [20, 0], [30, 0], [40, 0], [50, 0]]
# Randomly generate the x-coordinate of the apple
apple_x = randrange(-20, 18) * 10
# Randomly generate the y-coordinate of the apple
apple_y = randrange(-19, 19) * 10
# The snake's moving speed in the x-direction
aim_x = 0
# The snake's moving speed in the y-direction
aim_y = 10

# Record the time to control the key response interval
Time = time.time()

# Define a function to change the snake's moving direction
def change(x, y):
    global Time
    # Control the key response interval to avoid frequent direction changes
    if (time.time() - Time) > 0.07:
        global aim_y, aim_x
        # Ensure the new direction does not conflict with the current direction
        if x * aim_x >= 0:
            aim_x = x
        if y * aim_y >= 0:
            aim_y = y
        Time = time.time()

# Check if the snake has eaten itself
def inside_snake():
    for n in range(len(snake) - 1):
        if snake[-1][0] == snake[n][0] and snake[-1][1] == snake[n][1]:
            return True
    return False

# Check if the snake is within the map range
def inside_map():
    if -200 <= snake[-1][0] <= 180 and -190 <= snake[-1][1] <= 190:
        return True
    else:
        return False

# The main game loop function
def gameLoop():
    global apple_x, apple_y, aim_x, aim_y, snake
    # Move the snake forward by one grid
    snake.append([snake[-1][0] + aim_x, snake[-1][1] + aim_y])
    print(snake[-1][0], snake[-1][1])

    # If the snake does not eat the apple, remove the snake's tail
    if snake[-1][0] != apple_x or snake[-1][1] != apple_y:
        snake.pop(0)
    else:
        # The snake eats the apple, regenerate the apple's position
        apple_x = randrange(-20, 18) * 10
        apple_y = randrange(-19, 19) * 10

    # Check if the snake hits the wall or eats itself
    if (not inside_map()) or inside_snake():
        # Draw a red square to indicate the game is over
        square(snake[-1][0], snake[-1][1], 10, "red")
        update()
        sleep(2)
        # Reset the game parameters
        snake = [[0, 0], [10, 0], [20, 0], [30, 0], [40, 0], [50, 0]]
        apple_x = randrange(-20, 18) * 10
        apple_y = randrange(-19, 19) * 10
        aim_x = 0
        aim_y = 10

    clear()  # Clear the previously drawn graphics

    # Draw the game map boundary
    square(-210, -200, 410, "black")
    # Draw the inside of the game map
    square(-200, -190, 390, "white")
    # Draw the apple
    square(apple_x, apple_y, 10, "red")

    # Draw the snake's body
    for n in range(len(snake)):
        square(snake[n][0], snake[n][1], 10, "dark orange")

    update()  # Update the screen display

    # Call the main game loop function periodically
    ontimer(gameLoop, 200)

# Set the window size and position
setup(420, 420, 0, 0)
# Hide the pen arrow
hideturtle()
# Turn off automatic screen updates
tracer(False)
# Start listening for keyboard events
listen()

# Bind key events to change the snake's moving direction
onkey(lambda: change(0, 10), "w")
onkey(lambda: change(0, -10), "s")
onkey(lambda: change(-10, 0), "a")
onkey(lambda: change(10, 0), "d")

# Start the main game loop
gameLoop()
# Keep the window open
done()