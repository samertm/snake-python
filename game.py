from collections import deque, namedtuple
import random
import pygame

BOARD_LENGTH = 32
OFFSET = 16
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


DIRECTIONS = namedtuple('DIRECTIONS',
        ['Up', 'Down', 'Left', 'Right'])(0, 1, 2, 3)

def rand_color():
    return (random.randrange(254), random.randrange(254), random.randrange(254))

class Snake(object):
    def __init__(self, direction=DIRECTIONS.Right, 
            point=(0, 0, rand_color())):
        self.tailmax = 4
        self.direction = direction 
        self.deque = deque()
        self.deque.append(point)

def find_food(spots):
    while True:
        food = random.randrange(BOARD_LENGTH), random.randrange(BOARD_LENGTH)
        if (not (spots[food[0]][food[1]] == 1 or
            spots[food[0]][food[1]] == 2)):
            break
    return food


def end_condition(board, coord):
    if (coord[0] < 0 or coord[0] >= BOARD_LENGTH or coord[1] < 0 or
            coord[1] >= BOARD_LENGTH):
        return True
    if (board[coord[0]][coord[1]] == 1):
        return True
    return False

def make_board():
    spots = [[] for i in range(BOARD_LENGTH)]
    for row in spots:
        for i in range(BOARD_LENGTH):
            row.append(0)
    return spots
    

def update_board(screen, snake, food):
    rect = pygame.Rect(0, 0, OFFSET, OFFSET)

    spots = [[] for i in range(BOARD_LENGTH)]
    num1 = 0
    num2 = 0
    for row in spots:
        for i in range(BOARD_LENGTH):
            row.append(0)
            temprect = rect.move(num1 * OFFSET, num2 * OFFSET)
            pygame.draw.rect(screen, BLACK, temprect)
            num2 += 1
        num1 += 1
    spots[food[0]][food[1]] = 2
    temprect = rect.move(food[1] * OFFSET, food[0] * OFFSET)
    pygame.draw.rect(screen, WHITE, temprect)
    for coord in snake:
        spots[coord[0]][coord[1]] = 1
        temprect = rect.move(coord[1] * OFFSET, coord[0] * OFFSET)
        pygame.draw.rect(screen, coord[2], temprect)
    return spots


# Return 0 to exit the program, 1 for a one-player game
def menu(screen):
    menu_message = pygame.font.Font(None, 30).render("Press enter to start", True, WHITE)
    screen.fill(BLACK)
    screen.blit(menu_message, (32, 32)) 
    pygame.display.update()
    while True: 
        done = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quit given")
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    entered = True
                    return 1
        if done:
            break
    if done:
        pygame.quit()
        return 0

def quit(screen):
    return False

def change_direction(head, direction):
    if (direction == DIRECTIONS.Up):
        return (head[0] - 1, head[1], rand_color())
    elif (direction == DIRECTIONS.Down):
        return (head[0] + 1, head[1], rand_color())
    elif (direction == DIRECTIONS.Left):
        return (head[0], head[1] - 1, rand_color())
    elif (direction == DIRECTIONS.Right):
        return (head[0], head[1] + 1, rand_color())

def is_food(board, point):
    return board[point[0]][point[1]] == 2

def get_direction(events, prev_dir, identifier):
    if (identifier == "arrows"):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if prev_dir != DIRECTIONS.Down:
                        return DIRECTIONS.Up
                elif event.key == pygame.K_DOWN:
                    if prev_dir != DIRECTIONS.Up:
                        return DIRECTIONS.Down
                elif event.key == pygame.K_RIGHT:
                    if prev_dir != DIRECTIONS.Left:
                        return DIRECTIONS.Right
                elif event.key == pygame.K_LEFT:
                    if prev_dir != DIRECTIONS.Right:
                        return DIRECTIONS.Left
        return prev_dir
    if (identifier == "wasd"):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if prev_dir != DIRECTIONS.Down:
                        return DIRECTIONS.Up
                elif event.key == pygame.K_s:
                    if prev_dir != DIRECTIONS.Up:
                        return DIRECTIONS.Down
                elif event.key == pygame.K_a:
                    if prev_dir != DIRECTIONS.Left:
                        return DIRECTIONS.Right
                elif event.key == pygame.K_d:
                    if prev_dir != DIRECTIONS.Right:
                        return DIRECTIONS.Left
        return prev_dir


# Return false to quit program, true to go to
# gameover screen
def one_player(screen): 
    clock = pygame.time.Clock()
    spots = make_board()

    snake = Snake()
    # Board set up
    snake.deque.append((0, 0, rand_color()))
    spots[0][0] = 1
    food = find_food(spots)

    while True:
        clock.tick(15)
        # Event processing
        done = False
        events = pygame.event.get()
        for event in events: 
            if event.type == pygame.QUIT:
                print("Quit given")
                done = True
                break
        if done:
            return False
        snake.direction = get_direction(events, snake.direction, "arrows")

        # Game logic
        head = snake.deque.pop()
        next_head = change_direction(head, snake.direction)
        if (end_condition(spots, next_head)):
            return snake.tailmax

        if is_food(spots, next_head):
            snake.tailmax += 4
            food = find_food(spots)

        snake.deque.append(head)
        snake.deque.append(next_head)

        if len(snake.deque) > snake.tailmax:
            snake.deque.popleft()

        # Draw code
        screen.fill(BLACK)  # makes screen white

        spots = update_board(screen, snake.deque, food)

        pygame.display.update()

def two_player(screen):
    clock = pygame.time.Clock()
    spots = make_board()

    snakes = [Snake(), Snake(DIRECTIONS.Right, 
        (BOARD_LENGTH, BOARD_LENGTH, rand_color()))]
    
    


def game_over(screen, eaten):
    message1 = "You ate %d foods" % eaten
    game_over_message1 = pygame.font.Font(None, 30).render(message1, True, WHITE)
    message2 = "Press enter to play again, esc to quit."
    game_over_message2 = pygame.font.Font(None, 30).render(message2, True, WHITE)

    screen.blit(game_over_message1, (32, 32))
    screen.blit(game_over_message2, (62, 62))
    pygame.display.update()

    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_RETURN:
                    return True

 


def main():
    pygame.init()
    screen = pygame.display.set_mode([BOARD_LENGTH * OFFSET,
        BOARD_LENGTH * OFFSET])
    pygame.display.set_caption("Snaake")

    first = True
    playing = True
    while playing:
        if first:
            pick = menu(screen)

        options = {0 : quit,
                1 : one_player}
        now = options[pick](screen)
        if now == False:
            break
        else:
            eaten = now / 4 - 1
            playing = game_over(screen, eaten)
            first = False

    pygame.quit()

if __name__ == "__main__":
    main()
