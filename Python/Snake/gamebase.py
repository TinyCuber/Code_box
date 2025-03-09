from turtle import *

# Define a function to draw a square with specified position, size, and color
def square(x, y, size, color_name):
    up()  # Lift the pen, no drawing when moving
    goto(x, y)  # Move the pen to the specified coordinates
    down()  # Put down the pen, start drawing
    color(color_name)  # Set the pen and fill color
    begin_fill()  # Start filling color

    # Draw a square
    forward(size)
    left(90)
    forward(size)
    left(90)
    forward(size)
    left(90)
    forward(size)
    left(90)

    end_fill()  # End filling color