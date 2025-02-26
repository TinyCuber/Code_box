import pygame
from random import randrange
from time import sleep

pygame.init()


frame = 0
map_width = 284
map_height = 512
FPS = 60
pipes = [[180, 4]]
bird = [40, map_height // 2 - 50]
gravity = 0.2
velocity = 0

pipe_speed = 1

pass_count = 0

gameScreen = pygame.display.set_mode((map_width, map_height))
clock = pygame.time.Clock()

#Your path to the images
bird_wing_up = bird_wing_up_copy = pygame.image.load("images/bird_wing_up.png")
bird_wing_down = bird_wing_down_copy = pygame.image.load("images/bird_wing_down.png")
background = pygame.image.load("images/background.png")
pipe_body = pygame.image.load("images/pipe_body.png")
pipe_end = pygame.image.load("images/pipe_end.png")


input_text = ""

input_active = False

game_paused = False


def draw_pipes():
    global pipes, pipe_speed
    for n in range(len(pipes)):
        for m in range(pipes[n][1]):
            gameScreen.blit(pipe_body, (pipes[n][0], m * 32))
        for m in range(pipes[n][1] + 6, 16):
            gameScreen.blit(pipe_body, (pipes[n][0], m * 32))

        gameScreen.blit(pipe_end, (pipes[n][0], (pipes[n][1]) * 32))
        gameScreen.blit(pipe_end, (pipes[n][0], (pipes[n][1] + 5) * 32))
        pipes[n][0] -= pipe_speed

def draw_bird(x, y):
    global frame

    if 0 <= frame <= 30:
        gameScreen.blit(bird_wing_up, (x, y))
        frame += 1
    elif 30 < frame <= 60:
        gameScreen.blit(bird_wing_down, (x, y))
        frame += 1
        if frame == 60:
            frame = 0

def safe():
    if bird[1] > map_height - 35:
        print("hit floor")
        return False
    if bird[1] < 0:
        print("hit ceiling")
        return False
    if pipes[0][0] - 30 < bird[0] < pipes[0][0] + 79:
        if bird[1] < (pipes[0][1] + 1) * 32 or bird[1] > (pipes[0][1] + 4) * 32:
            print("hit pipe")
            return False
    return True

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

def gameLoop():
    global velocity, bird_wing_down, bird_wing_up, input_text, input_active, FPS, game_paused, pipe_speed, pass_count

    font = pygame.font.Font(None, 36)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        try:
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
                        bird[1] -= 40
                        velocity = 0
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if not game_paused:
            if len(pipes) < 4:
                x = pipes[-1][0] + 200
                open_pos = randrange(1, 9)
                pipes.append([x, open_pos])
            if pipes[0][0] < -80:
                pipes.pop(0)

            
            if pipes and bird[0] > pipes[0][0] + 79:
                pass_count += 1
                pipes.pop(0)

            velocity += gravity
            bird[1] += velocity
            bird_wing_down = pygame.transform.rotate(bird_wing_down_copy, -90 * (velocity / 15))
            bird_wing_up = pygame.transform.rotate(bird_wing_up_copy, -90 * (velocity / 15))

        gameScreen.blit(background, (0, 0))
        draw_pipes()
        draw_bird(bird[0], bird[1])

        
        pass_text = font.render(str(pass_count), True, (255, 255, 255))
        text_rect = pass_text.get_rect(topright=(map_width - 10, 10))
        gameScreen.blit(pass_text, text_rect)

        
        if input_active:
            text_surface = font.render(input_text, True, (255, 255, 255))
            gameScreen.blit(text_surface, (10, 10))
            pygame.draw.rect(gameScreen, (255, 255, 255), (10, 10, text_surface.get_width() + 10, text_surface.get_height() + 10), 2)

        pygame.display.update()
        if not game_paused and not safe():
            sleep(3)
            reset()
        clock.tick(FPS)


gameLoop()