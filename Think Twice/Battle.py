import pygame,sys
from button import Button
import puzzle
import pictureSelection
#gamePictures difficulty selection
SCREEN = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
BG = pygame.image.load("assets/pictures/ModelSelection.jpg")
#change BG size fo full screen
BG = pygame.transform.scale(BG, (1920, 1080))

STATUS = 1
pygame.init()

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def connect_success():
    STATUS = 1

#显示匹配中，等待对手
def wait_for_match():
    from main import main_menu
    import BattleClient
    SCREEN.blit(BG, (0, 0))
    # 更新页面
    pygame.display.update()
    OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
    OPTIONS_BACK = Button(image=None, pos=(300, 500),
                        text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
    OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
    OPTIONS_BACK.update(SCREEN)
    #显示assets/pictures/matching.gif
    matching = pygame.image.load("assets/pictures/match/matching.gif")
    matching = pygame.transform.scale(matching, (500, 500))
    SCREEN.blit(matching, (500, 200))
    pygame.display.update()
    #显示匹配中
    font = pygame.font.Font(None, 32)
    #等待对手
    BattleClient.main()
    # 等待1秒
    pygame.time.delay(5000)
    # 匹配成功，进入游戏
    if STATUS == 1:
        text_surface = font.render('Match success!', True, (255, 255, 255))
        SCREEN.blit(text_surface, (420, 490))
        pygame.display.flip()
    else:
        #匹配失败，返回主菜单
        text_surface = font.render('Match failed!', True, (255, 255, 255))
        SCREEN.blit(text_surface, (420, 490))
        pygame.display.flip()
        #等待1秒
        pygame.time.delay(1000)
        main_menu()



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        pygame.display.update()





