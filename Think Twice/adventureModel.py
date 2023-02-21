import threading,sys
import time
import pygame

import processBar
from button import Button
import math





flag = 0
BACKGROUNDLEVEL= 5
CURRENTLEVEL = 0

pygame.init()
SCREEN = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.FULLSCREEN)
BG = pygame.image.load("assets/pictures/background/adventure.png")
BG = pygame.transform.scale(BG, (pygame.display.Info().current_w, pygame.display.Info().current_h))


FPSCLOCK = pygame.time.Clock()
def islandModel():
    adv1 = pygame.image.load('assets/pictures/adventure/Background/' + str(BACKGROUNDLEVEL) + '.0.png')
    adv1 = pygame.transform.scale(adv1, (pygame.display.Info().current_w *15/ 18, pygame.display.Info().current_h *15/ 18))
    islandAnimation(adv1)




def islandAnimation(image):
    i = 0
    OPTIONS = [
        {'surf': pygame.image.load('assets/pictures/adventure/click.png'),
         'rect': pygame.Rect(pygame.display.Info().current_w / 8, pygame.display.Info().current_h * 13 / 32, 100,
                             100)},
        {'surf': pygame.image.load('assets/pictures/adventure/click.png'),
         'rect': pygame.Rect(pygame.display.Info().current_w / 3, pygame.display.Info().current_h * 15 / 32, 100,
                             100)},
        {'surf': pygame.image.load('assets/pictures/adventure/click.png'),
         'rect': pygame.Rect(pygame.display.Info().current_w * 17 / 36, pygame.display.Info().current_h * 10 / 32,
                             100, 100)},
        {'surf': pygame.image.load('assets/pictures/adventure/click.png'),
         'rect': pygame.Rect(pygame.display.Info().current_w * 43 / 72, pygame.display.Info().current_h * 14 / 32,
                             100, 100)},
        {'surf': pygame.image.load('assets/pictures/adventure/click.png'),
         'rect': pygame.Rect(pygame.display.Info().current_w * 57 / 72, pygame.display.Info().current_h * 12 / 32,
                             100, 100)},
    ]
    global CURRENTLEVEL,flag
    while True:
        j = 4*math.sin(i)
        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(image, (pygame.display.Info().current_w / 2 - image.get_width() / 2, pygame.display.Info().current_h / 2 - image.get_height() / 2 + j))

        i += 0.2
        for option in OPTIONS:
            #图片变透明
            SCREEN.blit(option['surf'], option['rect'])
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_BACK = Button(image=None,
                              pos=(pygame.display.Info().current_w * 1/2, pygame.display.Info().current_h *9 / 10),
                              text_input="BACK", font=get_font(60), base_color="White", hovering_color="Green")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
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
                    t = threading.Thread(target=processBar.processbarAnimation)
                    t.start()
                    t.join()
                    from main import main_menu
                    main_menu()
                if OPTIONS[0]['rect'].collidepoint(event.pos):
                    if BACKGROUNDLEVEL <= 5:
                        CURRENTLEVEL = 1
                        print('click1')
                        levelDetail()
                    else:
                        lockedLevel()
                if OPTIONS[1]['rect'].collidepoint(event.pos):
                    if BACKGROUNDLEVEL <= 4:
                        CURRENTLEVEL = 2
                        print('click2')
                        levelDetail()
                    else:
                        lockedLevel()



                if OPTIONS[2]['rect'].collidepoint(event.pos):
                    if BACKGROUNDLEVEL <= 3:
                        CURRENTLEVEL = 3
                        print('click3')
                        levelDetail()
                    else:
                        lockedLevel()



                if OPTIONS[3]['rect'].collidepoint(event.pos):
                    if BACKGROUNDLEVEL <= 2:
                        CURRENTLEVEL = 4
                        print('click4')
                        levelDetail()
                    else:
                        lockedLevel()


                if OPTIONS[4]['rect'].collidepoint(event.pos):
                    if BACKGROUNDLEVEL <= 1:
                        CURRENTLEVEL = 5
                        print('click5')
                        levelDetail()
                    else:
                        lockedLevel()
        pygame.display.update()



def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def lockedLevel():
    SCREEN.blit(BG, (0, 0))
    font = get_font(100)
    #red
    text = font.render("Locked", True, (255, 255, 255))
    lockImg = pygame.image.load('assets/pictures/adventure/未解锁.png')
    lockImg = pygame.transform.scale(lockImg, (pygame.display.Info().current_w / 4, pygame.display.Info().current_h /2))
    SCREEN.blit(lockImg, (pygame.display.Info().current_w / 2 - lockImg.get_width() / 2, pygame.display.Info().current_h*2/ 3 - lockImg.get_height()))
    SCREEN.blit(text, (pygame.display.Info().current_w / 2 - text.get_width() / 2, pygame.display.Info().current_h*2/ 3))
    pygame.display.update()
    time.sleep(1.5)





#滑块组件实现音量控制



#闯关模式
def adventureModel():
    #loadVideo()
    #processbarAnimation()
    record2()
    islandModel()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    return









#关卡详细界面
def levelDetail():
    global flag
    pic1 = pygame.image.load('assets/pictures/adventure/Level/gamePictures/p' + str(CURRENTLEVEL) + '.jpg')
    pic1 = pygame.transform.scale(pic1, (pygame.display.Info().current_h*2/3, pygame.display.Info().current_h*2/3))
    pic2 = pygame.image.load('assets/pictures/adventure/1星星.png')
    pic2 = pygame.transform.scale(pic2, (pygame.display.Info().current_h/3, pygame.display.Info().current_h/3))
    pic3 = pygame.image.load('assets/pictures/adventure/2星星.png')
    pic3 = pygame.transform.scale(pic3, (pygame.display.Info().current_h/3, pygame.display.Info().current_h/3))
    pic4 = pygame.image.load('assets/pictures/adventure/3星星.png')
    pic4 = pygame.transform.scale(pic4, (pygame.display.Info().current_h/3, pygame.display.Info().current_h/3))
    #难度系数text
    text = get_font(50).render("Difficulty:", True, (255, 0, 0))
    text1 = get_font(50).render("Level " + str(CURRENTLEVEL), True, (255, 255, 255))
    #show text and text1
    SCREEN.blit(BG, (0, 0))
    SCREEN.blit(text, (pygame.display.Info().current_w *9/ 20, pygame.display.Info().current_h / 2 - text.get_height() * 2))
    SCREEN.blit(text1, (pygame.display.Info().current_w *9/ 20 ,pygame.display.Info().current_h / 2 - text1.get_height() * 4))
    if CURRENTLEVEL <= 2:
        SCREEN.blit(pic2, (pygame.display.Info().current_w * 13 / 16, pygame.display.Info().current_h / 8))
    elif CURRENTLEVEL == 3:
        SCREEN.blit(pic3, (pygame.display.Info().current_w * 13 / 16, pygame.display.Info().current_h / 8))
    else:
        SCREEN.blit(pic4, (pygame.display.Info().current_w * 13 / 16, pygame.display.Info().current_h / 8))
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_BACK = Button(image=None, pos=(pygame.display.Info().current_w*3 / 4, pygame.display.Info().current_h *6/ 8),
                              text_input="BACK", font=get_font(60), base_color="White", hovering_color="Green")
        OPTIONS_START = Button(image=None, pos=(pygame.display.Info().current_w*3 / 4, pygame.display.Info().current_h *5/ 8),
                                 text_input="START", font=get_font(60), base_color="White", hovering_color="Green")

        OPTIONS_BACK.changeText(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        OPTIONS_START.changeText(OPTIONS_MOUSE_POS)
        OPTIONS_START.update(SCREEN)
        SCREEN.blit(pic1, (pygame.display.Info().current_h / 40, pygame.display.Info().current_h/2 - pic1.get_height()/2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    return
            #点击事件
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    print('back')
                    return
                if  OPTIONS_START.checkForInput(OPTIONS_MOUSE_POS):
                    record()
                    print('start')
                    path,level = levelInfo()
                    from puzzle import initial,main
                    initial(path,level)
                    main()
                    sys.exit()
        pygame.display.update()



def levelInfo():
    global CURRENTLEVEL
    #关卡信息
    level1 = 'assets/pictures/adventure/Level/gamePictures/p1.jpg'
    level2 = 'assets/pictures/adventure/Level/gamePictures/p2.jpg'
    level3 = 'assets/pictures/adventure/Level/gamePictures/p3.jpg'
    level4 = 'assets/pictures/adventure/Level/gamePictures/p4.jpg'
    level5 = 'assets/pictures/adventure/Level/gamePictures/p5.jpg'
    if CURRENTLEVEL == 1:
        return (level1,3)
    if CURRENTLEVEL == 2:
        return (level2,3)
    if CURRENTLEVEL == 3:
        return (level3,3)
    if CURRENTLEVEL == 4:
        return (level4,4)
    if CURRENTLEVEL == 5:
        return (level5,5)



def setBackGround():
    global BACKGROUNDLEVEL
    if BACKGROUNDLEVEL != 0:
        BACKGROUNDLEVEL -= 1
    return BACKGROUNDLEVEL

#读取BACKGROUNDLEVEL的值
def record2():
    global BACKGROUNDLEVEL
    f = open('assets/pictures/adventure/Level/record.txt', 'r')
    #接收第一行数据，用空格隔开
    data = f.readline().split(' ')
    BACKGROUNDLEVEL = int(data[0])
    f.close()


def record():
    global BACKGROUNDLEVEL, CURRENTLEVEL
    f = open('assets/pictures/adventure/Level/record.txt', 'w')
    f.write(str(BACKGROUNDLEVEL) + ' ' + str(CURRENTLEVEL))
    f.close()









adventureModel()