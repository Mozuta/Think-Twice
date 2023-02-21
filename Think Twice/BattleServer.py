import random
import socket
import threading
BLANK = None
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
NUM = 0



def getBlankPosition(board):
    global NUM
    # Return the x and y of board coordinates of the blank space.
    for x in range(NUM):
        for y in range(NUM):
            if board[x][y] == BLANK:
                return (x, y)

def generateNewPuzzle(numSlides):
    # From a starting configuration, make numSlides number of moves (and
    # animate these moves).
    board = getStartingBoard()
    sequence = []
    lastMove = None#numSlides*numSlides*10
    for i in range(3):
        move = getRandomMove(board, lastMove)
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return sequence

def getRandomMove(board, lastMove=None):
    # start with a full list of all four moves
    validMoves = [UP, DOWN, LEFT, RIGHT]
    # remove moves from the list as they are disqualified
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)

    # return a random move from the list of remaining moves
    return random.choice(validMoves)
def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)
def makeMove(board, move):
    # This function does not check if the move is valid.
    blankx, blanky = getBlankPosition(board)
    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


def getStartingBoard():
    global NUM
    # Return a board data structure with tiles in the solved state.
    # For example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
    # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
    counter = 1
    board = []
    for x in range(NUM):
        column = []
        for y in range(NUM):
            column.append(counter)
            counter += NUM
        board.append(column)
        counter -= NUM * (NUM - 1) + NUM - 1

    board[NUM-1][NUM-1] = BLANK
    return board

def client1():
    while 1:
        recv_message1=conn.recv(1024)
        conn1.send(recv_message1)
def client2():
    while 1:
        recv_message2=conn1.recv(1024)
        conn.send(recv_message2)

#接收两个客户端的NUM，若相等则开始游戏，否则提示重新输入
def getNum():
    global NUM, conn, conn1
    while 1:
        recv_message1 = conn.recv(1024)
        print("Client1:", recv_message1.decode())
        recv_message2 = conn1.recv(1024)
        print("Client2:", recv_message2.decode())
        if recv_message1 == recv_message2:
            NUM = int(recv_message1)
            break
        else:
            conn.send("Please input the same number".encode())
            conn1.send("Please input the same number".encode())
            continue



def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))  # 114.114.114.114也是dns地址
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip












s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host='192.168.55.191'
print(get_host_ip())
port=8000
s.bind((host,port))
s.listen(1)
print("Waiting for two connections, client1 and client2...")
conn, addr= s.accept()
print("Connected to client1!")
conn.send("Welcome to the server".encode())
print("Waiting for 2nd connection...")
conn1, addr= s.accept()
print("Connected to client2!")
conn1.send("Welcome to the server".encode())
getNum()


sequence = generateNewPuzzle(NUM)
#分别发送给两个客户端
conn.send(str(sequence).encode())
conn1.send(str(sequence).encode())


t1=threading.Thread(target=client1)
t2=threading.Thread(target=client2)
t1.start()
t2.start()





