import socket
import threading
import copy
import time

import processBar
from button import Button
import pygame, sys
from pygame.locals import *

BG = pygame.image.load("assets/pictures/background/puzzle.jpg")
# change BG size fo full screen
BG = pygame.transform.scale(BG, (pygame.display.Info().current_w, pygame.display.Info().current_h))
pygame.init()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

slideTo = None  # the direction, if any, a tile should slide
slideTo2 = None
STATE = None
BOARD = []
solutionSeq = []
# 空二维数组
mainBoard = []
CONTINUE = None


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def client():
    global s, slideTo2, STATE, BOARDWIDTH, solutionSeq, mainBoard, BOARD, CONTINUE
    # 获取WIFI的ip地址
    # ip = socket.gethostbyname(socket.gethostname())
    host = '192.168.55.191'

    port = 8000
    s.connect((host, port))
    print("Connected to the server")
    message = s.recv(1024)
    message = message.decode()
    print("Server message:", message)
    s.send(str(BOARDWIDTH).encode())
    while True:
        # 大缓存
        message = s.recv(2048)
        message = message.decode()
        print(message)
        if message != 'Please input the same number':
            # 去掉多余字符
            solutionSeq = str(message).replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(',')
            print(solutionSeq)
            break
    while 1:
        message = s.recv(1024)
        message = message.decode()
        print("Server message:", message)
        if message == "done":
            STATE = "lose"
        elif message == "next" or message == "back":
            CONTINUE = message
        else:
            slideTo2 = message

        print(message)


# Create the constants (go ahead and experiment with different values)
BOARDWIDTH = 4  # number of columns in the board
BOARDHEIGHT = 4  # number of rows in the board
TILESIZE = 130
IMAGEPATH = 'assets/pictures/adventure/Level/gamePictures/p5.jpg'

WINDOWWIDTH = pygame.display.Info().current_w
WINDOWHEIGHT = pygame.display.Info().current_h


# 全屏
def fullscreen():
    pygame.display.set_mode((1920, 1080), FULLSCREEN, 32)


FPS = 240
BLANK = None
IMAGES = []

TIME = 0
STEPS = 0
FIRSTSOLVE = True


def getImage(path):
    # Load the image and convert it to have alpha.
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, (TILESIZE * BOARDWIDTH, TILESIZE * BOARDHEIGHT))
    # convert the image
    image = image.convert_alpha()
    return image


# load image and split it into 3*3 tiles and store in IMAGES
def loadImages():
    # Load the image and convert it to have alpha.
    # image = pygame.image.load('assets/pictures/p6.jpg')
    # image = pygame.transform.scale(image, (TILESIZE*BOARDWIDTH, TILESIZE*BOARDHEIGHT))
    # image = image.convert_alpha()
    image = getImage(IMAGEPATH)
    # Calculate the width and height of each tile.
    imageWidth = int(image.get_width() / BOARDWIDTH)
    imageHeight = int(image.get_height() / BOARDHEIGHT)

    # Create each of the tiles.
    for tiley in range(BOARDHEIGHT):
        for tilex in range(BOARDWIDTH):
            left = tilex * imageWidth
            top = tiley * imageHeight
            tileImage = image.subsurface((left, top, imageWidth, imageHeight))
            IMAGES.append(tileImage)


#                 R    G    B
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHTBLUE = (0, 50, 255)
DARKTURQUOISE = (3, 54, 73)
GREEN = (0, 204, 0)

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = 200
YMARGIN = 50

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

allMoves = []  # list of moves made from the solved configuration

# show ORIGINAL image
# show original image on the screen

start = time.time()
msg = ''

def puzzleClient():
    global FPSCLOCK, STATE, allMoves, start, FIRSRSTART, slideTo, slideTo2, solutionSeq, mainBoard, BOARD, FIRSTSOLVE,  TIME, STEPS, ORIGINAL, DISPLAYSURF, OPTIONS, BASICFONT, PICTURESURF, NNM,msg,CONTINUE
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Slide Puzzle22222')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    # Store the option buttons and their rectangles in OPTIONS.
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    loadImages()
    SOLVEDBOARD = getStartingBoard()  # a solved board is the same as the board in a start state.

    t = threading.Thread(target=client)
    t.start()
    # 全屏显示assets/pictures/match/match.png
    matchimg = pygame.image.load('assets/pictures/match/match.png')
    matchimg = pygame.transform.scale(matchimg, (WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYSURF.blit(matchimg, (0, 0))
    MENU_TEXT = get_font(80).render("matching", True, 'white')
    MENU_RECT = MENU_TEXT.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT *6 / 8))
    DISPLAYSURF.blit(MENU_TEXT, MENU_RECT)
    pygame.display.update()
    frames = []
    for i in range(1, 20):
        img = pygame.image.load("assets/pictures/match/matching_gif/tenor(1)_wps图片_" + str(i) + ".png")
        img = pygame.transform.scale(img, (img.get_width() / 2, img.get_height() / 2))
        frames.append(img)
    while True:
        if solutionSeq != []:
            # 显示匹配成功
            success = pygame.image.load('assets/pictures/match/匹配成功.png')
            success = pygame.transform.scale(success, (400, 400))
            # 移除匹配中
            DISPLAYSURF.blit(matchimg, (0, 0))
            DISPLAYSURF.blit(success, (WINDOWWIDTH / 2 - 200, WINDOWHEIGHT / 2 - 300))
            count3 = pygame.image.load('assets/pictures/match/333.png')
            count3 = pygame.transform.scale(count3, (200, 250))
            DISPLAYSURF.blit(count3, (WINDOWWIDTH / 2 - 150, WINDOWHEIGHT / 2 + 150))
            pygame.display.update()
            time.sleep(10)

            DISPLAYSURF.blit(matchimg, (0, 0))
            DISPLAYSURF.blit(success, (WINDOWWIDTH / 2 - 200, WINDOWHEIGHT / 2 - 300))
            count2 = pygame.image.load('assets/pictures/match/222.png')
            count2 = pygame.transform.scale(count2, (200, 250))
            DISPLAYSURF.blit(count2, (WINDOWWIDTH / 2 - 150, WINDOWHEIGHT / 2 + 150))
            pygame.display.update()
            time.sleep(1)

            DISPLAYSURF.blit(matchimg, (0, 0))
            DISPLAYSURF.blit(success, (WINDOWWIDTH / 2 - 200, WINDOWHEIGHT / 2 - 300))
            count2 = pygame.image.load('assets/pictures/match/111.png')
            count2 = pygame.transform.scale(count2, (200, 250))
            DISPLAYSURF.blit(count2, (WINDOWWIDTH / 2 - 150, WINDOWHEIGHT / 2 + 150))
            pygame.display.update()
            time.sleep(1)
            mainBoard = createNewPuzzle(solutionSeq)
            BOARD = copy.deepcopy(mainBoard)
            break
        else:
            for frame in frames:
                checkForQuit()
                DISPLAYSURF.blit(frame, (pygame.display.Info().current_w / 2 - frame.get_width() / 2, pygame.display.Info().current_h / 2 - frame.get_height() / 2))
                pygame.display.update()
                FPSCLOCK.tick(int(FPS / 10))
        # 防止程序未响应
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        FPSCLOCK.tick(FPS)

    FIRSRSTART = True
    while True:  # main gamePictures loop
        # 开始计时
        if FIRSRSTART:
            start = time.time()
            FIRSRSTART = False

        slideTo = None
        msg = 'Click tile or press arrow keys to slide.'  # contains the message to show in the upper left corner.
        if mainBoard == SOLVEDBOARD:
            msg = 'Solved!'
            s.send('done'.encode())
        if STATE == 'lose':
            msg = 'lose!'
        state = drawBoard(mainBoard, msg)
        if state == 'solved':
            message = solved()
            if message == 'next':
                while CONTINUE != 'next' and CONTINUE != 'back':
                    # 显示等待对方选择
                    DISPLAYSURF.blit(matchimg, (0, 0))
                    MENU_TEXT = get_font(30).render("Waiting opponent to response...", True, 'white')
                    MENU_RECT = MENU_TEXT.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT * 6 / 8))
                    DISPLAYSURF.blit(MENU_TEXT, MENU_RECT)
                    for frame in frames:
                        checkForQuit()
                        DISPLAYSURF.blit(frame, (pygame.display.Info().current_w / 2 - frame.get_width() / 2,
                                                 pygame.display.Info().current_h / 2 - frame.get_height() / 2))
                        FPSCLOCK.tick(int(FPS / 10))
                        pygame.display.update()
                        if CONTINUE == 'next' or CONTINUE == 'back':
                            break
                        FPSCLOCK.tick(int(FPS / 10))
                    # 防止程序未响应
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == KEYUP:
                            if event.key == K_ESCAPE:
                                pygame.quit()
                                sys.exit()
                if CONTINUE == 'next':
                    DISPLAYSURF.blit(matchimg, (0, 0))
                    DISPLAYSURF.blit(success, (WINDOWWIDTH / 2 - 200, WINDOWHEIGHT / 2 - 300))
                    count3 = pygame.image.load('assets/pictures/match/333.png')
                    count3 = pygame.transform.scale(count3, (200, 250))
                    DISPLAYSURF.blit(count3, (WINDOWWIDTH / 2 - 150, WINDOWHEIGHT / 2 + 150))
                    pygame.display.update()
                    time.sleep(1)

                    DISPLAYSURF.blit(matchimg, (0, 0))
                    DISPLAYSURF.blit(success, (WINDOWWIDTH / 2 - 200, WINDOWHEIGHT / 2 - 300))
                    count2 = pygame.image.load('assets/pictures/match/222.png')
                    count2 = pygame.transform.scale(count2, (200, 250))
                    DISPLAYSURF.blit(count2, (WINDOWWIDTH / 2 - 150, WINDOWHEIGHT / 2 + 150))
                    pygame.display.update()
                    time.sleep(1)

                    DISPLAYSURF.blit(matchimg, (0, 0))
                    DISPLAYSURF.blit(success, (WINDOWWIDTH / 2 - 200, WINDOWHEIGHT / 2 - 300))
                    count2 = pygame.image.load('assets/pictures/match/111.png')
                    count2 = pygame.transform.scale(count2, (200, 250))
                    DISPLAYSURF.blit(count2, (WINDOWWIDTH / 2 - 150, WINDOWHEIGHT / 2 + 150))
                    pygame.display.update()
                    time.sleep(1)



                    mainBoard = createNewPuzzle(solutionSeq)
                    BOARD = copy.deepcopy(mainBoard)
                    start = time.time()
                    msg = 'Click tile or press arrow keys to slide.'
                    STATE = None
                    CONTINUE = None
                    slideTo = None
                    text = BASICFONT.render('Time: %s' % (str(round(time.time() - start, 2))), True, TEXTCOLOR)
                    textRect = text.get_rect()
                    textRect.center = (50, 50)
                    # 更新时间
                    DISPLAYSURF.blit(text, textRect)
                    pygame.display.update()
                    #回到while循环
                    continue
                elif CONTINUE == 'back':
                    # 显示对方已离开
                    DISPLAYSURF.blit(matchimg, (0, 0))
                    noAnswering = pygame.image.load('assets/pictures/match/noAnswering.png')
                    noAnswering = pygame.transform.scale(noAnswering, (WINDOWWIDTH / 3, WINDOWHEIGHT / 3))
                    MENU_TEXT = get_font(30).render("The opponent has left", True, 'white')
                    MENU_RECT = MENU_TEXT.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT * 6 / 8))
                    DISPLAYSURF.blit(MENU_TEXT, MENU_RECT)
                    DISPLAYSURF.blit(noAnswering, (WINDOWWIDTH *2/ 6, WINDOWHEIGHT / 4))
                    pygame.display.update()
                    while True:
                        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
                        OPTIONS_BACK = Button(image=None, pos=(WINDOWWIDTH - 400, WINDOWHEIGHT - 100),
                                              text_input="BACK", font=get_font(50), base_color="White",
                                              hovering_color="Green")
                        OPTIONS_BACK.changeText(OPTIONS_MOUSE_POS)
                        OPTIONS_BACK.update(DISPLAYSURF)
                        pygame.display.update()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                                    pygame.mixer.Sound("assets/music/sound effect/bt_tile_click.mp3").play()
                                    t = threading.Thread(target=processBar.processbarAnimation)
                                    t.start()
                                    t.join()
                                    from main import main_menu
                                    main_menu()
                                    sys.exit()
            elif message == 'back':
                t = threading.Thread(target=processBar.processbarAnimation)
                t.start()
                t.join()
                from main import main_menu
                main_menu()
                sys.exit()


        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])
                if (spotx, spoty) != (None, None):
                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                        STEPS += 1
                        s.send('left'.encode())
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                        STEPS += 1
                        s.send('right'.encode())
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                        STEPS += 1
                        s.send('up'.encode())
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN
                        STEPS += 1
                        s.send('down'.encode())

            elif event.type == KEYUP:
                # check if the user pressed a key to slide a tile
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo2 = LEFT
                    # 向服务器发送移动信息
                    s.send('left'.encode())
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo2 = RIGHT
                    s.send('right'.encode())

                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo2 = UP
                    s.send('up'.encode())

                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo2 = DOWN
                    s.send('down'.encode())

        if slideTo:
            slideAnimation(mainBoard, slideTo, 'Click tile or press arrow keys to slide.', 8, 1)  # show slide on screen
            pygame.mixer.Sound("assets/music/sound effect/bt_tile_click.mp3").play()
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo)  # record the slide

        if slideTo2:
            # slideAnimation(BOARD, slideTo2, 'Click tile or press arrow keys to slide.', 8,2)
            makeMove(BOARD, slideTo2)
            slideTo2 = None

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def solved():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_BACK = Button(image=None, pos=(WINDOWWIDTH - 200, WINDOWHEIGHT - 200),
                              text_input="BACK", font=get_font(50), base_color="White", hovering_color="Green")
        OPTIONS_BACK.changeText(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(DISPLAYSURF)
        OPTIONS_NEXT = Button(image=None, pos=(WINDOWWIDTH - 200, WINDOWHEIGHT - 300),
                              text_input="NEXT", font=get_font(50), base_color="White", hovering_color="Green")
        OPTIONS_NEXT.changeText(OPTIONS_MOUSE_POS)
        OPTIONS_NEXT.update(DISPLAYSURF)
        pygame.display.update()
        # 接收数据

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    s.send('back'.encode())
                    return 'back'
                if OPTIONS_NEXT.checkForInput(OPTIONS_MOUSE_POS):
                    s.send('next'.encode())
                    return 'next'

        pygame.display.update()


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):  # get all the QUIT events
        terminate()  # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP):  # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate()  # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event)  # put the other KEYUP event objects back


def getStartingBoard():
    # Return a board data structure with tiles in the solved state.
    # For example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
    # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1
    board[BOARDWIDTH - 1][BOARDWIDTH - 1] = BLANK
    return board


def getBlankPosition(board):
    # Return the x and y of board coordinates of the blank space.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                return (x, y)


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


def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)


def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)


def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    # draw IMAGES to the screen
    DISPLAYSURF.blit(IMAGES[number - 1], (left + adjx, top + adjy))
    # textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    # textRect = textSurf.get_rect()
    # textRect.center = left + adjx, top + adjy
    # #show the IMAGES
    # DISPLAYSURF.blit(textSurf, textRect)


def drawTile2(tilex, tiley, number, adjx=0, adjy=0):
    left, top = getLeftTopOfTile(tilex, tiley)
    DISPLAYSURF.blit(IMAGES[number - 1], (left + adjx + WINDOWWIDTH*3/8, top + adjy))


def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def drawBoard(board, message):
    global BOARD
    DISPLAYSURF.blit(BG, (0, 0))
    stepsSurf = BASICFONT.render('Steps: %s' % (STEPS), True, TEXTCOLOR)
    stepsRect = stepsSurf.get_rect()
    stepsRect.topleft = (0, 70)
    DISPLAYSURF.blit(stepsSurf, stepsRect)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)
        if message == "Solved!":
            pygame.mixer.music.load("assets/music/sound effect/升级_胜利.mp3")
            pygame.mixer.music.play()
            winAnimation(5)
            return 'solved'
        if message == "lose!":
            pygame.mixer.music.load("assets/music/sound effect/游戏结束.mp3")
            pygame.mixer.music.play()
            loseAnimation(5)
            return 'solved'

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])
    for tilex in range(len(BOARD)):
        for tiley in range(len(BOARD[0])):
            if BOARD[tilex][tiley]:
                drawTile2(tilex, tiley, BOARD[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)
    ORIGINAL = pygame.image.load(IMAGEPATH)
    ORIGINAL = pygame.transform.scale(ORIGINAL, (TILESIZE, TILESIZE))
    DISPLAYSURF.blit(ORIGINAL, (WINDOWWIDTH - ORIGINAL.get_width(), 0))


def slideAnimation(board, direction, message, animationSpeed, type):
    # Note: This function does not check if the move is valid.

    blankx, blanky = getBlankPosition(board)
    movex = None
    movey = None
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    # prepare the base surface
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    # transparant = pygame.Surface((TILESIZE, TILESIZE))
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    baseSurf.set_alpha(50)
    pygame.draw.rect(baseSurf, (0, 0, 0), (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if type == 1:
            if direction == UP:
                drawTile(movex, movey, board[movex][movey], 0, -i)
            if direction == DOWN:
                drawTile(movex, movey, board[movex][movey], 0, i)
            if direction == LEFT:
                drawTile(movex, movey, board[movex][movey], -i, 0)
            if direction == RIGHT:
                drawTile(movex, movey, board[movex][movey], i, 0)
        elif type == 2:
            if direction == UP:
                drawTile2(movex, movey, board[movex][movey], 0, -i)
            if direction == DOWN:
                drawTile2(movex, movey, board[movex][movey], 0, i)
            if direction == LEFT:
                drawTile2(movex, movey, board[movex][movey], -i, 0)
            if direction == RIGHT:
                drawTile2(movex, movey, board[movex][movey], i, 0)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def loseAnimation(animationSpeed):
    lose = pygame.image.load("assets/pictures/match/lose.png")
    lose = pygame.transform.scale(lose, (pygame.display.Info().current_w / 2, pygame.display.Info().current_h / 2))
    TILESIZE = lose.get_width()
    for i in range(0, TILESIZE, animationSpeed):
        checkForQuit()
        DISPLAYSURF.blit(BG, (0, 0))
        DISPLAYSURF.blit(lose, (WINDOWWIDTH / 2 - TILESIZE, WINDOWHEIGHT - i))
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def winAnimation(animationSpeed):
    win = pygame.image.load("assets/pictures/match/win.png")
    win = pygame.transform.scale(win, (pygame.display.Info().current_w / 2, pygame.display.Info().current_h / 2))
    TILESIZE = win.get_width()
    for i in range(0, TILESIZE, animationSpeed):
        checkForQuit()
        DISPLAYSURF.blit(BG, (0, 0))
        DISPLAYSURF.blit(win, (WINDOWWIDTH / 2 - TILESIZE, WINDOWHEIGHT - i))
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def createNewPuzzle(sequence):
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500)  # pause 500 milliseconds for effect
    for i in range(len(sequence)):
        move = sequence[i]
        slideAnimation(board, move, 'Generating new puzzle...', animationSpeed=int(TILESIZE / 3), type=1)
        makeMove(board, move)
    return board


def resetAnimation(board, allMoves):
    revAllMoves = allMoves[:]  # gets a copy of the list
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slideAnimation(board, oppositeMove, '', animationSpeed=int(TILESIZE / 2), type=1)
        makeMove(board, oppositeMove)


puzzleClient()