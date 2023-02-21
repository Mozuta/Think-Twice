import threading
import pygame, sys, random
from pygame.locals import *
import time
import copy
from button import Button
import processBar



pygame.init()
BG = pygame.image.load("assets/pictures/background/puzzle.jpg")
#change BG size fo full screen
BG = pygame.transform.scale(BG, (pygame.display.Info().current_w, pygame.display.Info().current_h))



BOARDWIDTH = 3  # number of columns in the board
BOARDHEIGHT = 3 # number of rows in the board
TILESIZE = 250
IMAGEPATH = 'assets/pictures/p6.jpg'
WINDOWWIDTH = pygame.display.Info().current_w
WINDOWHEIGHT = pygame.display.Info().current_h
PATTERN = 2




FPS = 240
BLANK = None
IMAGES = []
TIME = 0
STEPS = 0
FIRSTSOLVE = True
mainBoard = []






#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)

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
allMoves = []# list of moves made from the solved configuration
SOLVEDBOARD = []
GENERATEDBOAD = []
TIME = 0
FIRSRSTART = True

def main():
    global FPSCLOCK,allMoves,FIRSTSOLVE,IMAGES,mainBoard,START_SURF, START_RECT, TIME,STEPS,ORIGINAL,DISPLAYSURF, OPTIONS,BASICFONT,PICTURESURF,NNM,TIME,FIRSRSTART
    FIRSRSTART = True
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    # Store the option buttons and their rectangles in OPTIONS.
    DISPLAYSURF = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h),pygame.FULLSCREEN, 32)
    OPTIONS = [
        {'surf': pygame.image.load('assets/pictures/adventure/重来1.png'), 'rect': pygame.Rect(72, WINDOWHEIGHT*3/8, 100, 100),'text': '重来'},
        {'surf': pygame.image.load('assets/pictures/adventure/菜单1.png'), 'rect': pygame.Rect(72, WINDOWHEIGHT/4, 100, 100),'text': '菜单'},
        {'surf': pygame.image.load('assets/pictures/adventure/音乐1.png'), 'rect': pygame.Rect(72, WINDOWHEIGHT/8, 100, 100),'text': '音乐'},
    ]
    loadImages()
    mainBoard, solutionSeq = generateNewPuzzle(3,1)
    GENERATEDBOAD = copy.deepcopy(mainBoard)
    SOLVEDBOARD = getStartingBoard() # a solved board is the same as the board in a start state.

    while True:  # main gamePictures loop
        # 开始计时
        if FIRSRSTART:
            start = time.time()
            FIRSRSTART = False
        TIME = str(round(time.time() - start, 2))


        slideTo = None # the direction, if any, a tile should slide
        msg = 'Click tile or press arrow keys to slide.' # contains the message to show in the upper left corner.



        if mainBoard == SOLVEDBOARD:
            msg = 'Solved!'
        state = drawBoard(mainBoard, msg)
        if state == 'end':
            print('end')
            break
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONDOWN:
                optionsEvent(event.pos,0)
            if event.type == MOUSEBUTTONUP:
                optionsEvent(event.pos,1)
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])
                if (spotx, spoty) != (None, None):
                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                        STEPS += 1
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                        STEPS += 1
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                        STEPS += 1
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN
                        STEPS += 1

            elif event.type == KEYUP:
                # check if the user pressed a key to slide a tile
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN
        if slideTo:
            slideAnimation(mainBoard, slideTo, 'Click tile or press arrow keys to slide.', 20) # show slide on screen
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo) # record the slide
        pygame.display.update()
        FPSCLOCK.tick(FPS)




def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back


def getStartingBoard():
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

    board[BOARDWIDTH-1][BOARDHEIGHT-1] = BLANK
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
    pygame.mixer.Sound("assets/music/sound effect/bt_tile_click.mp3").play()
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
    left, top = getLeftTopOfTile(tilex, tiley)
    DISPLAYSURF.blit(IMAGES[number-1], (left + adjx, top + adjy))

    #Text Tips
    # textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    # textRect = textSurf.get_rect()
    # textRect.center = left + adjx, top + adjy
    # DISPLAYSURF.blit(textSurf, textRect)









def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def drawBoard(board, message):
    global STEPS,TIME,PATTERN,TIME
    DISPLAYSURF.blit(BG, (0, 0))
    text = BASICFONT.render('Time: ' + str(TIME), True, TEXTCOLOR)
    textRect = text.get_rect()
    textRect.topleft = (0, 50)
    DISPLAYSURF.blit(text, textRect)
    stepsSurf = BASICFONT.render('Steps: %s' % (STEPS), True, TEXTCOLOR)
    stepsRect = stepsSurf.get_rect()
    stepsRect.topleft = (0, 70)
    DISPLAYSURF.blit(stepsSurf, stepsRect)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)
        if message == "Solved!":
            pygame.mixer.Sound("assets/music/sound effect/bt_tile_click.mp3").play()
            if PATTERN == 2:
                pygame.mixer.music.load("assets/music/sound effect/升级_胜利.mp3")
                pygame.mixer.music.play()
                solvedAnimation()
            elif PATTERN == 1:
                #播放音效
                pygame.mixer.music.load("assets/music/sound effect/升级_胜利.mp3")
                pygame.mixer.music.play()
                solved2()
            return 'end'

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)
    # Original image
    ORIGINAL = pygame.image.load(IMAGEPATH)
    ORIGINAL = pygame.transform.scale(ORIGINAL, (TILESIZE*8/5, TILESIZE*8/5))
    DISPLAYSURF.blit(ORIGINAL, (WINDOWWIDTH - ORIGINAL.get_width(), 0))
    for option in OPTIONS:
        DISPLAYSURF.blit(option['surf'], option['rect'])


def optionsEvent(event,type):
    global allMoves,mainBoard,IMAGES,STEPS,TIME,PATTERN,FIRSRSTART
    if type == 0:
        for option in OPTIONS:
            if option['rect'].collidepoint(event):
                if option['text'] == '重来':
                    option['surf'] = pygame.image.load("assets/pictures/adventure/重来0.png")
                elif option['text'] == '菜单':
                    option['surf'] = pygame.image.load("assets/pictures/adventure/菜单0.png")
                elif option['text'] == '音乐':
                    option['surf'] = pygame.image.load("assets/pictures/adventure/音乐0.png")
    if type == 1:
        for option in OPTIONS:
            if option['rect'].collidepoint(event):
                if option['text'] == '重来':
                    resetAnimation(mainBoard, allMoves)
                    allMoves = []
                    STEPS = 0
                    TIME = 0
                    FIRSRSTART = True
                    option['surf'] = pygame.image.load("assets/pictures/adventure/重来1.png")
                    print("重来")

                elif option['text'] == '菜单':
                    option['surf'] = pygame.image.load("assets/pictures/adventure/菜单1.png")
                    pygame.mixer.Sound("assets/music/sound effect/bt_tile_click.mp3").play()
                    print("菜单")
                    IMAGES = []
                    STEPS = 0
                    TIME = 0
                    FIRSRSTART = True
                    if PATTERN == 1:
                        t = threading.Thread(target=processBar.processbarAnimation)
                        t.start()
                        t.join()
                        from adventureModel import adventureModel
                        adventureModel()
                        sys.exit()
                    elif PATTERN == 2:
                        t = threading.Thread(target=processBar.processbarAnimation)
                        t.start()
                        t.join()
                        from pictureSelection import picture_selection
                        picture_selection()
                        sys.exit()
                elif option['text'] == '音乐':
                    option['surf'] = pygame.image.load("assets/pictures/adventure/音乐1.png")
                    #如果音乐开着，就暂停
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    print("音乐")





def solvedAnimation():
    #原图中心放大
    global ORIGINAL,IMAGES,STEPS,TIME,PATTERN,IMAGEPATH
    ORIGINAL = pygame.image.load(IMAGEPATH)
    ORIGINAL = pygame.transform.scale(ORIGINAL, (TILESIZE/4,TILESIZE/4))
    originalSurf = ORIGINAL.copy()
    originalSurf2 = pygame.image.load(IMAGEPATH)
    originalSurf2 = pygame.transform.scale(originalSurf2, (TILESIZE * 59 / 30, TILESIZE * 59 / 30))
    for i in range(70):
        scale = 1 + (i * 0.1)
        originalSurf = pygame.transform.scale(originalSurf, (int(ORIGINAL.get_width() * scale), int(ORIGINAL.get_height() * scale)))
        DISPLAYSURF.blit(originalSurf,(WINDOWWIDTH / 4 - originalSurf.get_width() / 2, WINDOWHEIGHT / 2 - originalSurf.get_height()*3/ 4 ))
        if i == 69:
            DISPLAYSURF.blit(originalSurf2, (
            WINDOWWIDTH / 4 - originalSurf.get_width() / 2, WINDOWHEIGHT / 2 - originalSurf.get_height() * 3 / 4))
        pygame.display.update()
        pygame.time.wait(5)
    #pygame.time.wait(500)
    #YouWin = pygame.image.load("assets/pictures/you_win.jpg")
    #YouWin = pygame.transform.scale(YouWin, (WINDOWWIDTH / 4,WINDOWHEIGHT / 4))
    #DISPLAYSURF.blit(YouWin, (WINDOWWIDTH *3/4 , 0))
    userName = inputName()
    if userName == '':
        userName = 'player'
    print("done")
    saveRecord(userName, score(float(BOARDWIDTH), float(STEPS), float(TIME)))
    print("done2")
    #返回主界面按钮
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_BACK = Button(image=None, pos=(WINDOWWIDTH *7/ 8, WINDOWHEIGHT *7/ 8),
                              text_input="BACK", font=get_font(70), base_color="White", hovering_color="Green")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(DISPLAYSURF)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    IMAGES = []
                    STEPS = 0
                    TIME = 0
                    if PATTERN == 1:
                        changeLevel()
                        t = threading.Thread(target=processBar.processbarAnimation)
                        t.start()
                        t.join()
                        from adventureModel import adventureModel
                        adventureModel()
                        sys.exit()
                    elif PATTERN == 2:
                        t = threading.Thread(target=processBar.processbarAnimation)
                        t.start()
                        t.join()
                        from pictureSelection import picture_selection
                        picture_selection()
                        sys.exit()

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)
#提示用户输入名字
def inputName():
    text_input = pygame.Rect(WINDOWWIDTH*3 / 5, WINDOWHEIGHT / 2-30, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    # 文本输入框内容
    text = ''
    font = pygame.font.Font(None, 32)
    # label 请输入你的名字
    label = get_font(35).render('Please enter your name', True, '#00ffff')
    #你的分数
    Score = get_font(35).render('Your score is ' + str(score(float(BOARDWIDTH), float(STEPS), float(TIME))), True, '#00ffff')
    done = False
    #记录成功
    success = get_font(33).render('Record successfully saved', True, '#00ffff')
    originalSurf2 = pygame.image.load(IMAGEPATH)
    originalSurf2 = pygame.transform.scale(originalSurf2, (WINDOWWIDTH / 4, WINDOWWIDTH / 4))
    while not done:
        DISPLAYSURF.blit(BG, (0,0))
        DISPLAYSURF.blit(label, (WINDOWWIDTH * 7 / 16, WINDOWHEIGHT / 4 - text_input.height+130))
        DISPLAYSURF.blit(Score, (WINDOWWIDTH * 7 / 16, WINDOWHEIGHT / 4 - text_input.height - label.get_height()+100))
        MENU_TEXT = get_font(80).render("Congratulations!", True, colortwinkle())
        MENU_RECT = MENU_TEXT.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT * 1 / 8))
        DISPLAYSURF.blit(MENU_TEXT, MENU_RECT)
        DISPLAYSURF.blit(originalSurf2, (
            WINDOWWIDTH / 4 - originalSurf2.get_width() / 2, WINDOWHEIGHT / 2 - originalSurf2.get_height() * 2 / 4))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                # If the user clicked on the input_box rect.
                if text_input.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        done = True
                        DISPLAYSURF.blit(success, (WINDOWWIDTH * 7 / 16, WINDOWHEIGHT / 2 + text_input.height+160))
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        text_input.w = width
        # Blit the text.
        DISPLAYSURF.blit(txt_surface, (text_input.x + 5, text_input.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(DISPLAYSURF, color, text_input, 2)
        pygame.display.update()
        if done:
            return text









def slideAnimation(board, direction, message, animationSpeed):
    # Note: This function does not check if the move is valid.

    blankx, blanky = getBlankPosition(board)
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
    #transparant = pygame.Surface((TILESIZE, TILESIZE))
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    baseSurf.set_alpha(50)
    pygame.draw.rect(baseSurf, (0,0,0), (moveLeft, moveTop, TILESIZE, TILESIZE))


    for i in range(0, TILESIZE, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)
        pygame.display.update()
        FPSCLOCK.tick(FPS)



def generateNewPuzzle(numSlides,type):
    # From a starting configuration, make numSlides number of moves (and
    # animate these moves).
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500) # pause 500 milliseconds for effect
    lastMove = None
    if type == 1:
        for i in range(numSlides):
            move = getRandomMove(board, lastMove)
            slideAnimation(board, move, 'Generating new puzzle...', animationSpeed=int(TILESIZE / 3))
            makeMove(board, move)
            sequence.append(move)
            lastMove = move
    return (board, sequence)


def resetAnimation(board, allMoves):
    # make all of the moves in allMoves in reverse.
    if allMoves != []:
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
            slideAnimation(board, oppositeMove, '', animationSpeed=int(TILESIZE / 2))
            makeMove(board, oppositeMove)




def score(gai,y_step,y_time):
    std_step=gai*gai*5
    std_time =(gai - 2) * (gai - 2) * 60
    fin_score=1e4+(std_step-y_step)*3+(std_time-y_time)*10
    return fin_score

def saveRecord(userName,fin_score):
    with open('record.txt','a') as f:
        f.write(str(userName)+' '+str(fin_score)+'\n')





def getImage(path):
    # Load the image and convert it to have alpha.
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, (TILESIZE * BOARDWIDTH, TILESIZE * BOARDHEIGHT))
    image = image.convert_alpha()
    return image

#load image and split it into 3*3 tiles and store in IMAGES
def loadImages():
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

def initial(path,NUM):
    global BOARDWIDTH,BOARDHEIGHT,IMAGEPATH,TILESIZE,IMAGES,PATTERN,allMoves,STEPS
    BOARDWIDTH = NUM
    BOARDHEIGHT = NUM
    IMAGEPATH = path
    TILESIZE = int(750 / NUM)
    IMAGES = []
    PATTERN = 1
    allMoves = []
    STEPS = 0
    main()

#修改assets/pictures/adventure/Level/record.txt里的值
def changeLevel():
    with open('assets/pictures/adventure/Level/record.txt','r') as f:
        record=f.read()
        record=record.split(' ')
    data1 = int(record[0])
    data2 = int(record[1])

    if data1 + data2 == 6:
        with open('assets/pictures/adventure/Level/record.txt', 'w') as f:
            f.write(str(int(record[0]) - 1) + ' ' + str(6 -int(record[0])))




#闯关模式结算
def solved2():
    global IMAGEPATH
    original = pygame.image.load(IMAGEPATH)
    original = pygame.transform.scale(original, (TILESIZE * 9 / 5, TILESIZE * 9 / 5))
    while True:
        DISPLAYSURF.blit(BG, (0, 0))
        DISPLAYSURF.blit(original, (WINDOWWIDTH /8, WINDOWHEIGHT / 4))
        MENU_TEXT = get_font(80).render("Congratulations!", True, colortwinkle())
        MENU_RECT = MENU_TEXT.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT * 1 / 8))
        DISPLAYSURF.blit(MENU_TEXT, MENU_RECT)
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_BACK = Button(image=None,
                              pos=(pygame.display.Info().current_w * 3 / 4, pygame.display.Info().current_h * 6 / 8),
                              text_input="BACK", font=get_font(60), base_color="White", hovering_color="Green")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(DISPLAYSURF)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    return
            # 点击事件
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    changeLevel()
                    pygame.mixer.music.load("assets/music/bgm/mode_3_desert.mp3")
                    pygame.mixer.music.play(-1)
                    t = threading.Thread(target=processBar.processbarAnimation)
                    t.start()
                    t.join()
                    from adventureModel import adventureModel
                    adventureModel()
                    sys.exit()



def colortwinkle():
    for i in range(1, 10):
        t = time.time()
        q = int(t * 10 % 10)
        if q == 0:
            return ('#00fa9a')
        if q == 1:
            return ('#9370db')
        if q == 2:
            return ('#ba55d3')
        if q == 3:
            return ('#f0e68c')
        if q == 4:
            return ('#ccff00')
        if q == 5:
            return ('#f08080')
        if q == 6:
            return ('#ffffe0')
        if q == 7:
            return ('#f400a1')
        if q == 8:
            return ('#ffd700')
        if q == 9:
            return ('#00ffff')




