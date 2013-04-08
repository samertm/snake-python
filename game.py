import sys
import collections
import time
import random

BOARD_LENGTH = 32

class Directions:
    Up, Down, Left, Right = range(4)

def prettyprint(x):
    for row in x:
        for col in row:
            print(col, end='')
        print(end='\n')

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

def updateBoard(snake, food):
    spots = [[] for i in range(BOARD_LENGTH)]
    for row in spots:
        for i in range(BOARD_LENGTH):
            row.append(0)
    spots[food[0]][food[1]] = 2
    for coord in snake:
        spots[coord[0]][coord[1]] = 1
    return spots

def main():
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
#    food = findFood(spots)
#   for debugging
    food = 0,6
    spots[food[0]][food[1]] = 2
    prettyprint(spots)

    while True:
        currtime = time.time()
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
            break

        if spots[nextHead[0]][nextHead[1]] == 2:
            tailmax += 4
            food = findFood(spots)

        snake.append(head)
        snake.append(nextHead)
        
        if len(snake) > tailmax:
            tail = snake.popleft()
        
        spots = updateBoard(snake, food)
        prettyprint(spots)

        while (time.time() - currtime < .5):
            time.sleep(.1)

if __name__ == "__main__":
    main()
