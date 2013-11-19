import socket
import select
import time
import datetime
import random
from collections import deque, namedtuple

BOARD_LENGTH = 32
OFFSET = 16
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

DIRECTIONS = namedtuple('DIRECTIONS',
        ['Up', 'Down', 'Left', 'Right'])(0, 1, 2, 3)

SNAKE_STATE = namedtuple('SNAKE_STATE', ['Alive', 'Dead'])(0, 1)

class Snake(object):
    def __init__(self, direction=DIRECTIONS.Right, 
                 point=(0, 0, RED), color=None):
        self.tailmax = 4
        self.direction = direction 
        self.deque = deque()
        self.deque.append(point)
        self.color = color
        self.nextDir = deque()
        self.state = SNAKE_STATE.Alive
    
    def get_color(self):
        if self.color is None:
            return rand_color()
        else:
            return self.color

    # for the client    
    # def populate_nextDir(self, events, identifier):
    #     if (identifier == "arrows"):
    #         for event in events:
    #             if event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.K_UP:
    #                     self.nextDir.appendleft(DIRECTIONS.Up)
    #                 elif event.key == pygame.K_DOWN:
    #                     self.nextDir.appendleft(DIRECTIONS.Down)
    #                 elif event.key == pygame.K_RIGHT:
    #                     self.nextDir.appendleft(DIRECTIONS.Right)
    #                 elif event.key == pygame.K_LEFT:
    #                     self.nextDir.appendleft(DIRECTIONS.Left)
    #     if (identifier == "wasd"):
    #         for event in events:
    #             if event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.K_w:
    #                     self.nextDir.appendleft(DIRECTIONS.Up)
    #                 elif event.key == pygame.K_s:
    #                     self.nextDir.appendleft(DIRECTIONS.Down)
    #                 elif event.key == pygame.K_d:
    #                     self.nextDir.appendleft(DIRECTIONS.Right)
    #                 elif event.key == pygame.K_a:
    #                     self.nextDir.appendleft(DIRECTIONS.Left)

def find_point(spots):
    while True:
        point = random.randrange(BOARD_LENGTH), random.randrange(BOARD_LENGTH)
        if (not (spots[point[0]][point[1]] == 1 or
            spots[point[0]][point[1]] == 2)):
            break
    return point


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


def network_nextDirs(net_data, num_snakes):
    moves = []
    for i in range(num_snakes):
        moves.append(deque())
    while net_data != "":
        #net_data comes in the form
        #'1l0r1u'
        snake_id = int(net_data[0])
        snake_dir = net_data[1]
        if snake_dir == "u":
            moves[snake_id].appendleft(DIRECTIONS.Up)
        elif snake_dir == "d":
            moves[snake_id].appendleft(DIRECTIONS.Down)
        elif snake_dir == "r":
            moves[snake_id].appendleft(DIRECTIONS.Right)
        elif snake_dir == "l":
            moves[snake_id].appendleft(DIRECTIONS.Left)
        net_data = net_data[2:]
    return moves

            
def move(snake):
    if len(snake.nextDir) != 0:
        next_dir = snake.nextDir.pop()
    else:
        next_dir = snake.direction
    head = snake.deque.pop()
    snake.deque.append(head)
    next_move = head
    if (next_dir == DIRECTIONS.Up):
        if snake.direction != DIRECTIONS.Down:
            next_move =  (head[0] - 1, head[1], snake.get_color())
            snake.direction = next_dir
        else:
            next_move =  (head[0] + 1, head[1], snake.get_color())
    elif (next_dir == DIRECTIONS.Down):
        if snake.direction != DIRECTIONS.Up:
            next_move =  (head[0] + 1, head[1], snake.get_color())
            snake.direction = next_dir
        else:
            next_move =  (head[0] - 1, head[1], snake.get_color())
    elif (next_dir == DIRECTIONS.Left):
        if snake.direction != DIRECTIONS.Right:
            next_move =  (head[0], head[1] - 1, snake.get_color())
            snake.direction = next_dir
        else:
            next_move =  (head[0], head[1] + 1, snake.get_color())
    elif (next_dir == DIRECTIONS.Right):
        if snake.direction != DIRECTIONS.Left:
            next_move =  (head[0], head[1] + 1, snake.get_color())
            snake.direction = next_dir
        else:
            next_move =  (head[0], head[1] - 1, snake.get_color())
    return next_move

def encode_point(point, obj):
    # makes a string of the form
    # (15 23 bk)
    enc_str = "(" + str(point[0]) + " " + str(point[1])
    if obj == "snake":
        if point[2] == RED:
            enc_str += " rd)"
        elif point[2] == WHITE:
            enc_str += " wh)"
        elif point[2] == BLACK:
            enc_str += " bk)"
        elif point[2] == BLUE:
            enc_str += " bl)"
    elif obj == "food":
        enc_str += " fo)"
    elif obj == "remove":
        enc_str += " rm)"
    return enc_str

def network_update_board(snakes, food):
    # update_board with all the drawing code removed
    spots = [[] for i in range(BOARD_LENGTH)]
    for row in spots:
        for i in range(BOARD_LENGTH):
            row.append(0)
    spots[food[0]][food[1]] = 2
    for snake in snakes:
        for coord in snake.deque:
            spots[coord[0]][coord[1]] = 1
    return spots

def is_food(board, point):
    return board[point[0]][point[1]] == 2


def snake_server(): 
    HOST, PORT = "162.243.37.26", 9999
    num_snakes = 2
    spots = make_board()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(2)

    snakes = [Snake(DIRECTIONS.Right, (0, 0, RED), RED), Snake(DIRECTIONS.Right, (5, 5, BLUE), BLUE)]
    
    socks = []
    for i in range(num_snakes):
        socks.append(s.accept())
        print("connected {}".format(i))

    for i, s in enumerate(socks):
        socks[i] = s[0]
        s[0].sendall("{}".format(i).encode("utf-8"))
        s[0].setblocking(False)

    send_data = ""
    for snake in snakes:
        point = snake.deque.pop()
        spots[point[0]][point[1]] = 1
        send_data += encode_point(point, "snake")
        snake.deque.append(point)
    
    food = find_point(spots)
    send_data += encode_point(food, "food")

    time_stamp = datetime.datetime.now()
    time.sleep(0.15)            # just in case...
    
    while True:
        # overview of the game loop:
        # send add/remove data to clients
        # calculate framerate
        # check for data from clients
        # parse client data & append data to snake objects
        # run game logic & create send_data

        # send add/remove data to clients
        _polls, writes, _exceps = select.select([], socks, [], 0)
        for w in writes:
            w.sendall(send_data.encode("utf-8"))

        # calculate framerate
        at_framerate = False
        while not at_framerate:
            temp_time = datetime.datetime.now()
            time_delta = ((temp_time.minute * 60000000 + temp_time.second * 1000000 + temp_time.microsecond) -
                          (time_stamp.minute *60000000 + time_stamp.second *1000000 + time_stamp.microsecond))
            if time_delta > 70000:
                at_framerate = True
            else:
                time.sleep((70000 - time_delta) / 1000000)
        time_stamp = temp_time

        # check for data from clients        
        polls, _writes, _excep = select.select(socks, [], [], 0)
        poll_data = b""
        for p in polls:
            poll_data += p.recv(1024)
        if poll_data != "":
            poll_data = poll_data.decode("utf-8")

        # parse client data & append data to snake objects
        moves = network_nextDirs(poll_data, num_snakes) # parse next dirs
        
        # append network directions to internal directions
        for i, m in enumerate(moves):
            while len(m) > 0:
                snakes[i].nextDir.appendleft(m.pop())

        # run game logic & create send_data                
        send_data = ""
        for snake in snakes:
            if snake.state == SNAKE_STATE.Alive:
                next_head = move(snake)
                if (end_condition(spots, next_head)):
                    snake.state = SNAKE_STATE.Dead
                    break
                    
                if is_food(spots, next_head):
                    snake.tailmax += 4
                    food = find_point(spots)
                    
                snake.deque.append(next_head)
                send_data += encode_point(next_head, "snake")
            
                if len(snake.deque) > snake.tailmax:
                    remove_point = snake.deque.popleft()
                    send_data += encode_point(remove_point, "remove")
                    
                send_data += encode_point(food, "food")
            elif snake.state == SNAKE_STATE.Dead:
                if len(snake.deque) == 0:
                    snake.direction = DIRECTIONS.Right
                    point = find_point(spots)
                    new_head = (point[0], point[1], snake.get_color())
                    snake.tailmax = 4
                    snake.deque.append(new_head)
                    snake.state = SNAKE_STATE.Alive
                    send_data += encode_point(new_head, "snake")
                else:
                    remove_point = snake.deque.popleft()
                    send_data += encode_point(remove_point, "remove")

        spots = network_update_board(snakes, food)
    for i in socks:
        i.shutdown(socket.SHUT_RDWR)
        i.close()
            
if __name__ == "__main__":
    snake_server()
