import pygame
from random import randrange
from time import sleep

# Initialize the Pygame library
pygame.init()

# Initialize game variables
frame = 0
map_width = 284
map_height = 512
FPS = 60
# Initial position and opening position of pipes
pipes = [[180, 4]]
# Initial position of the bird
bird = [40, map_height // 2 - 50]
# Gravitational acceleration
gravity = 0.2
# Bird's velocity
velocity = 0

# Pipe movement speed
pipe_speed = 1

# Count of the bird passing through pipes
pass_count = 0

# Create the game window
gameScreen = pygame.display.set_mode((map_width, map_height))
# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Load game image resources
# Image of the bird with wings up
# Write your path of the images
bird_wing_up = bird_wing_up_copy = pygame.image.load("images/bird_wing_up.png")
# Image of the bird with wings down
bird_wing_down = bird_wing_down_copy = pygame.image.load("images/bird_wing_down.png")
# Game background image
background = pygame.image.load("images/background.png")
# Pipe body image
pipe_body = pygame.image.load("images/pipe_body.png")
# Pipe top and bottom image
pipe_end = pygame.image.load("images/pipe_end.png")

# User input text
input_text = ""

# Whether the input box is active
input_active = False

# Whether the game is paused
game_paused = False

# Function to draw pipes
def draw_pipes():
    global pipes, pipe_speed
    for n in range(len(pipes)):
        # Draw the upper part of the pipe
        for m in range(pipes[n][1]):
            gameScreen.blit(pipe_body, (pipes[n][0], m * 32))
        # Draw the lower part of the pipe
        for m in range(pipes[n][1] + 6, 16):
            gameScreen.blit(pipe_body, (pipes[n][0], m * 32))

        # Draw the top and bottom of the pipe
        gameScreen.blit(pipe_end, (pipes[n][0], (pipes[n][1]) * 32))
        gameScreen.blit(pipe_end, (pipes[n][0], (pipes[n][1] + 5) * 32))
        # Move the pipe
        pipes[n][0] -= pipe_speed

# Function to draw the bird
def draw_bird(x, y):
    global frame
    # Draw the bird in different postures according to the frame
    if 0 <= frame <= 30:
        gameScreen.blit(bird_wing_up, (x, y))
        frame += 1
    elif 30 < frame <= 60:
        gameScreen.blit(bird_wing_down, (x, y))
        frame += 1
        if frame == 60:
            frame = 0

# Function to check if the bird is safe
def safe():
    # Check if the bird hits the floor
    if bird[1] > map_height - 35:
        print("hit floor")
        return False
    # Check if the bird hits the ceiling
    if bird[1] < 0:
        print("hit ceiling")
        return False
    # Check if the bird hits the pipe
    if pipes[0][0] - 30 < bird[0] < pipes[0][0] + 79:
        if bird[1] < (pipes[0][1] + 1) * 32 or bird[1] > (pipes[0][1] + 4) * 32:
            print("hit pipe")
            return False
    return True

# Function to reset the game
def reset():
    global frame, map_width, map_height, FPS, pipes, bird, gravity, velocity, pipe_speed, pass_count
    frame = 0
    map_width = 284
    map_height = 512
    FPS = 60
    pipes.clear()
    bird.clear()
    pipes = [[180, 4]]
    bird = [40, map_height // 2 - 50]
    gravity = 0.2
    velocity = 0
    pipe_speed = 1
    pass_count = 0

# Main game loop function
def gameLoop():
    global velocity, bird_wing_down, bird_wing_up, input_text, input_active, FPS, game_paused, pipe_speed, pass_count

    # Create a font object
    font = pygame.font.Font(None, 36)
    while True:
        # Handle game events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if input_active:
                    # Handle user input
                    if event.key == pygame.K_RETURN:
                        try:
                            # Convert the input text to a floating-point number as the new pipe speed
                            new_speed = float(input_text)
                            if new_speed > 0:
                                pipe_speed = new_speed
                            input_text = ""
                            input_active = False
                            game_paused = False
                        except ValueError:
                            input_text = ""
                            input_active = False
                            game_paused = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
                elif event.key == pygame.K_RETURN:
                    input_active = True
                    game_paused = True
                else:
                    if not game_paused:
                        # The bird flies upwards
                        bird[1] -= 40
                        velocity = 0
            if event.type == pygame.QUIT:
                # Quit the game
                pygame.quit()
                return

        if not game_paused:
            # Generate new pipes
            if len(pipes) < 4:
                x = pipes[-1][0] + 200
                open_pos = randrange(1, 9)
                pipes.append([x, open_pos])
            # Remove pipes that are out of the screen
            if pipes[0][0] < -80:
                pipes.pop(0)

            # Count the number of times the bird passes through pipes
            if pipes and bird[0] > pipes[0][0] + 79:
                pass_count += 1
                pipes.pop(0)

            # Update the bird's velocity and position
            velocity += gravity
            bird[1] += velocity
            # Rotate the bird's image according to its velocity
            bird_wing_down = pygame.transform.rotate(bird_wing_down_copy, -90 * (velocity / 15))
            bird_wing_up = pygame.transform.rotate(bird_wing_up_copy, -90 * (velocity / 15))

        # Draw the background
        gameScreen.blit(background, (0, 0))
        # Draw the pipes
        draw_pipes()
        # Draw the bird
        draw_bird(bird[0], bird[1])

        # Draw the count of passing through pipes
        pass_text = font.render(str(pass_count), True, (255, 255, 255))
        text_rect = pass_text.get_rect(topright=(map_width - 10, 10))
        gameScreen.blit(pass_text, text_rect)

        # Draw the input box
        if input_active:
            text_surface = font.render(input_text, True, (255, 255, 255))
            gameScreen.blit(text_surface, (10, 10))
            pygame.draw.rect(gameScreen, (255, 255, 255), (10, 10, text_surface.get_width() + 10, text_surface.get_height() + 10), 2)

        # Update the display
        pygame.display.update()
        # Check if the bird is safe. If not, reset the game
        if not game_paused and not safe():
            sleep(3)
            reset()
        # Control the frame rate
        clock.tick(FPS)

# Start the main game loop
gameLoop()