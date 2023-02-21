import pygame
from button import Button
import time

pygame.init()
SCREEN = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.FULLSCREEN)
BG = pygame.image.load("assets/pictures/Rank.png")
BG = pygame.transform.scale(BG, (pygame.display.Info().current_w, pygame.display.Info().current_h))
FPS = 40

FPSCLOCK = pygame.time.Clock()

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def showRank():
    flag_sound1 = False
    #显示排行榜
    SCREEN.blit(BG, (0, 0))
    #显示姓名和分数
    name, score = get_font(50).render('Name', True, (0,  50, 255)), get_font(50).render('Score', True,(0,  50, 255))
    SCREEN.blit(name, (pygame.display.Info().current_w/ 6, pygame.display.Info().current_h*4/20))
    SCREEN.blit(score, (pygame.display.Info().current_w / 2 , pygame.display.Info().current_h*4/20))
    readRank()
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_BACK = Button(image=None, pos=(pygame.display.Info().current_w *10/20, pygame.display.Info().current_h - 90),
                              text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
        OPTIONS_BACK.changeText(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        if flag_sound1 == False and OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
            pygame.mixer.Sound("assets/music/sound effect/bt_menu_click.mp3").play()
            flag_sound1 = True
        # mouse not hovering over the play button, sound effect will not play
        if flag_sound1 == True and not OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
            flag_sound1 = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    pygame.mixer.Sound("assets/music/sound effect/bt_tile_click.mp3").play()
                    from ModelSelection import gameDifficulty
                    gameDifficulty()
        pygame.display.update()

#读取文件
def readRank():
    #读取排行榜record.txt
    with open('record.txt', 'r') as f:
        dict = {}
        #读取每一行的内容，第一个是名字，第二个是分数,按分数从大到小排序
        for line in f.readlines():
            line = line.strip()
            name, score = line.split(' ')
            #存入字典两位小数
            if name in dict:
                dict[name] = str(max(float(dict[name]), float(score)))
            else:
                dict[name] = str(float(score))
        #分数转换成float类型然后排序
        dict = sorted(dict.items(), key=lambda x: float(x[1]), reverse=True)
        #显示前十名
        if len(dict) > 10:
            NUM = 10
        else:
            NUM = len(dict)
        pos = 0
        for i in range(NUM):
            name, score = get_font(50).render(dict[i][0], True, (255, 255, 255)), get_font(50).render(dict[i][1], True,(255, 255, 255))
            # 显示在SCREEN上
            SCREEN.blit(name, (pygame.display.Info().current_w/ 6, 300 + pos))
            SCREEN.blit(score, (pygame.display.Info().current_w / 2, 300 + pos))
            time.sleep(0.3)
            pos += name.get_height()
            pygame.display.update()
