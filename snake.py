import pygame
import random
pygame.font.init()

#Font family
pygame.display.set_caption("Snake Game")
LOSS_FONT = pygame.font.SysFont('comicsans', 50)
SCORE_FONT = pygame.font.SysFont('comicsans', 30)

#Screen
FPS = 60
WIDTH = 400
HEIGHT = 340
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#Snake
HIT_YOURSELF = pygame.USEREVENT + 1
TIME_TO_FASTER = 30
SNAKE_VEL = 40

#Food stuff
FOOD_WIDTH = SNAKE_WIDTH = 20
BIG_FOOD_WIDTH = FOOD_WIDTH*3
APPLE_IMG = pygame.image.load('apple.jpg')
BIG_APPLE_IMG = pygame.image.load('bigapple.jpg')
APPLE = pygame.transform.scale(APPLE_IMG, (FOOD_WIDTH - 3, FOOD_WIDTH))# minus 3 to make the apple less "fat"
BIG_APPLE = pygame.transform.scale(BIG_APPLE_IMG, (BIG_FOOD_WIDTH, BIG_FOOD_WIDTH))

#Color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 170, 0)
LIGHT_GREEN = (1, 208, 29)
RED = (255, 0, 0)

class Snake:
    def __init__(self, x, y, direction):
        self.square = pygame.Rect(x, y, SNAKE_WIDTH, SNAKE_WIDTH)
        self.direction = direction


def draw_screen(snake, food, score):
    score_text = SCORE_FONT.render(f'Score: {score}', 1, BLACK)
    screen.fill(WHITE)
    screen.blit(APPLE, (food.x, food.y))

    pygame.draw.rect(screen, LIGHT_GREEN, snake[-1].square)
    for i in range(len(snake) - 2, 0, -1):
        pygame.draw.rect(screen, GREEN, snake[i].square)
    pygame.draw.rect(screen, DARK_GREEN, snake[0].square)

    screen.blit(score_text, (WIDTH - 15 - score_text.get_width(), 15))

    pygame.display.update()

def draw_loss(draw_text):
    text = LOSS_FONT.render(draw_text, 1, BLACK)
    screen.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def get_move(head, keys_pressed):
    if keys_pressed[pygame.K_LEFT]:  # left
        head.direction = 'left'
    if keys_pressed[pygame.K_RIGHT]:  # right
        head.direction = 'right'
    if keys_pressed[pygame.K_UP]:  # up
        head.direction = 'up'
    if keys_pressed[pygame.K_DOWN]:  # down
        head.direction = 'down'

def moving_same_direction(first_part, second_part):#make the snake doesn't go the opposite way
    if first_part.direction == 'left' and second_part.direction == 'right':
        pass
    elif first_part.direction == 'right' and second_part.direction == 'left':
        pass
    elif first_part.direction == 'up' and second_part.direction == 'down':
        pass
    elif first_part.direction == 'down' and second_part.direction == 'up':
        pass
    else:
        first_part.direction = second_part.direction

def move(body_part):#use for body parts except the head
    if body_part.direction == 'left':
        body_part.square.x -= SNAKE_WIDTH
    elif body_part.direction == 'right':
        body_part.square.x += SNAKE_WIDTH
    elif body_part.direction == 'up':
        body_part.square.y -= SNAKE_WIDTH
    elif body_part.direction == 'down':
        body_part.square.y += SNAKE_WIDTH

def head_move(snake):#use for the head
    if snake[0].direction == 'left' and snake[0].square.x - SNAKE_WIDTH >= 0:
        if snake[2].direction != 'right':
            snake[0].square.x -= SNAKE_WIDTH
        else:
            snake[0].direction = 'right'
            snake[0].square.x += SNAKE_WIDTH
    elif snake[0].direction == 'right' and snake[0].square.x + SNAKE_WIDTH + SNAKE_WIDTH <= WIDTH:
        if snake[2].direction != 'left':
            snake[0].square.x += SNAKE_WIDTH
        else:
            snake[0].direction = 'left'
            snake[0].square.x -= SNAKE_WIDTH
    elif snake[0].direction == 'up' and snake[0].square.y - SNAKE_WIDTH >= 0:
        if snake[2].direction != 'down':
            snake[0].square.y -= SNAKE_WIDTH
        else:
            snake[0].direction = 'down'
            snake[0].square.y += SNAKE_WIDTH
    elif snake[0].direction == 'down' and snake[0].square.y + SNAKE_WIDTH + SNAKE_WIDTH <= HEIGHT:
        if snake[2].direction != 'up':
            snake[0].square.y += SNAKE_WIDTH
        else:
            snake[0].direction = 'up'
            snake[0].square.y -= SNAKE_WIDTH
    else:
        raise IndexError

def get_hit(snake):
    for i in range(1, len(snake)):
        if snake[0].square.colliderect(snake[i].square):
            pygame.event.post(pygame.event.Event(HIT_YOURSELF))

def check_food(snake, food):
    for body in snake:
        if food.colliderect(body.square):
            return False
    return True

def create_random_food(snake):
    while True:# while the food appear in the snake
        x_co = random.randint(0, WIDTH / FOOD_WIDTH-1) * FOOD_WIDTH# which in this case is food width
        y_co = random.randint(0, HEIGHT / FOOD_WIDTH-1) * FOOD_WIDTH
        food = pygame.Rect(x_co, y_co, SNAKE_WIDTH, SNAKE_WIDTH)
        if check_food(snake, food):
            break
    return food

def eat_food(snake, food):
    if snake[0].square.x == food.x and snake[0].square.y == food.y:
        return True
    return False

def add_part(snake):
    if snake[-1].direction == 'right':
        x = snake[-1].square.x - SNAKE_WIDTH
        y = snake[-1].square.y
    elif snake[-1].direction == 'left':
        x = snake[-1].square.x + SNAKE_WIDTH
        y = snake[-1].square.y
    elif snake[-1].direction == 'up':
        x = snake[-1].square.x
        y = snake[-1].square.y + SNAKE_WIDTH
    elif snake[-1].direction == 'down':
        x = snake[-1].square.x
        y = snake[-1].square.y - SNAKE_WIDTH
    return x, y

def main():
    global SNAKE_VEL#to speed up the snake after a period of time

    x_start, y_start = (SNAKE_WIDTH*((WIDTH/2)//SNAKE_WIDTH), 
                        SNAKE_WIDTH*((HEIGHT/2)//SNAKE_WIDTH))

    head = Snake(x_start, y_start, 'right')
    b1 = Snake(x_start - SNAKE_WIDTH, y_start, 'right')
    b2 = Snake(x_start - 2*SNAKE_WIDTH, y_start, 'right')
    snake = [head, b1, b2]

    food = create_random_food(snake)

    score = 0

    clock = pygame.time.Clock()
    start_time = 0
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == HIT_YOURSELF:
                draw_text = 'Oops, you hit yourself!'
                draw_loss(draw_text)
                running = False

        keys_pressed = pygame.key.get_pressed()
        get_move(head, keys_pressed)
        #make the snake move
        if start_time % SNAKE_VEL == 0:
            for i in range(len(snake)-1, 0, -1):
                move(snake[i])
                moving_same_direction(snake[i], snake[i-1])
            try:
                head_move(snake)
            except IndexError:#if the head touch the border
                draw_text = 'You hit the wall =(('
                draw_loss(draw_text)
                running = False

        if eat_food(snake, food):
            #add body part
            x, y = add_part(snake)
            body = Snake(x, y, direction = snake[-1].direction)
            snake.append(body)
            #add food
            food = create_random_food(snake)
            #add score
            score += 10
            #move faster if the snake is too long
            if len(snake) % 5 == 0 and SNAKE_VEL > 2:
                SNAKE_VEL -= 2

        # if start_time > (30*60) and start_time % (TIME_TO_FASTER*60) == 0:
        #     SNAKE_VEL -= 1

        get_hit(snake)  # check if the snake touch itself
        draw_screen(snake, food, score)
        start_time += 1

    pygame.quit()

if __name__ == '__main__':
    main()