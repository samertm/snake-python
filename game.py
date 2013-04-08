import sys
import collections
import time
import random
import pygame

BOARD_LENGTH = 32
OFFSET = 16

class Directions:
    Up, Down, Left, Right = range(4)

def findFood(spots):
    while True:
        food = random.randrange(BOARD_LENGTH), random.randrange(BOARD_LENGTH)
        if (not (spots[food[0]][food[1]] == 1 or spots[food[0]][food[1]] == 2)):
            break
    return food
    
def endCondition(board, coord):
    if (coord[0] < 0 or coord[0] >= BOARD_LENGTH or coord[1] < 0 or coord[1] >= BOARD_LENGTH):
        return True
    if (board[coord[0]][coord[1]] == 1): 
        return True
    return False

def updateBoard(screen, snake, food):
    white = (255, 255, 255)
    black = (0, 0, 0)

    rect = pygame.Rect(0,0,OFFSET,OFFSET)
    
    spots = [[] for i in range(BOARD_LENGTH)]
    num1 = 0
    num2 = 0
    for row in spots:
        for i in range(BOARD_LENGTH):
            row.append(0)
            temprect = rect.move(num1*OFFSET,num2*OFFSET) 
            pygame.draw.rect(screen, white, temprect)
            num2 += 1
        num1 += 1
    spots[food[0]][food[1]] = 2
    temprect = rect.move(food[1]*OFFSET, food[0]*OFFSET)
    pygame.draw.rect(screen, black, temprect)
    for coord in snake:
        spots[coord[0]][coord[1]] = 1
        temprect = rect.move(coord[1]*OFFSET, coord[0]*OFFSET)
        pygame.draw.rect(screen, black, temprect)
    return spots

def main():
    pygame.init()
    screen = pygame.display.set_mode([BOARD_LENGTH*OFFSET, BOARD_LENGTH*OFFSET])
    pygame.display.set_caption("Snaake")
    clock = pygame.time.Clock()

    spots = [[] for i in range(BOARD_LENGTH)]
    for row in spots:
        for i in range(BOARD_LENGTH):
            row.append(0)
    
    # Board set up
    tailmax = 4
    direction = Directions.Right
    snake = collections.deque()
    snake.append((0,0))
    spots[0][0] = 1
    food = findFood(spots)
    spots[food[0]][food[1]] = 2

    while True:
        # Event processing 
        done = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quit given")
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if direction != Directions.Down:
                         direction = Directions.Up
                elif event.key == pygame.K_DOWN:
                    if direction != Directions.Up:
                         direction = Directions.Down
                elif event.key == pygame.K_RIGHT:
                    if direction != Directions.Left:
                         direction = Directions.Right
                elif event.key == pygame.K_LEFT:
                    if direction != Directions.Right:
                         direction = Directions.Left


        if done:
            break

        # Game logic
        head = snake.pop()
        if (direction == Directions.Up):
            nextHead = (head[0] - 1, head[1])
        elif (direction == Directions.Down):
            nextHead = (head[0] + 1, head[1])
        elif (direction == Directions.Left):
            nextHead = (head[0], head[1] - 1)
        elif (direction == Directions.Right):
            nextHead = (head[0], head[1] + 1)
        if (endCondition(spots, nextHead)):
            print(nextHead)
            print("end condition reached")
            break

        if spots[nextHead[0]][nextHead[1]] == 2:
            tailmax += 4
            food = findFood(spots)

        snake.append(head)
        snake.append(nextHead)
        
        if len(snake) > tailmax:
            tail = snake.popleft()

        # Draw code
        black = (0,0,0)
        white = (255, 255, 255)
        screen.fill(white) # makes screen white
        
        spots = updateBoard(screen, snake, food)


#        pygame.draw.line(screen, white, (60, 60), (120, 60), 4)
        pygame.display.update()

        clock.tick(20)
    pygame.quit()

if __name__ == "__main__":
    main()
