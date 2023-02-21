import pygame
pygame.init()
SCREEN = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.FULLSCREEN)
BG = pygame.image.load("assets/pictures/background/adventure.jpg")
BG = pygame.transform.scale(BG, (pygame.display.Info().current_w, pygame.display.Info().current_h))
FPS = 100
FPSCLOCK = pygame.time.Clock()
# def processbarAnimation():
#
#     emptyBar = pygame.image.load('assets/pictures/adventure/进度条空.png')
#     TILESIZE = emptyBar.get_width()
#     mask = pygame.image.load('assets/pictures/adventure/进度条遮挡.png')
#
#     #i不为TILESIZE时，进度条不满
#     i = 0
#     while i < TILESIZE:
#         SCREEN.blit(BG, (0, 0))
#         SCREEN.blit(emptyBar, (pygame.display.Info().current_w / 2 - emptyBar.get_width() / 2,pygame.display.Info().current_h - emptyBar.get_height()))
#         fullBar = pygame.image.load('assets/pictures/adventure/进度条满.png')
#         fullBar = pygame.transform.scale(fullBar, (i, fullBar.get_height()))
#         SCREEN.blit(fullBar, (pygame.display.Info().current_w / 2 -TILESIZE/2, pygame.display.Info().current_h - fullBar.get_height()-23))
#         SCREEN.blit(mask, (pygame.display.Info().current_w / 2 - emptyBar.get_width() / 2 - mask.get_width()/2,pygame.display.Info().current_h - mask.get_height()*1.25))
#         pygame.display.update()
#         FPSCLOCK.tick(FPS)
#         if i < TILESIZE/4:
#             i += 2
#         elif i < TILESIZE/4*2:
#             i += 5
#         elif i < TILESIZE/4*3:
#             i += 0.5
#         else:
#             i +=5
#     print(TILESIZE)
#     return

def processbarAnimation():

    emptyBar = pygame.image.load('assets/pictures/adventure/进度条空.png')
    girla = pygame.image.load('assets/pictures/adventure/图层 5.png')
    atk = pygame.image.load('assets/pictures/adventure/图层 7.png')
    atk2 = pygame.image.load('assets/pictures/adventure/图层 7.png')
    TILESIZE = emptyBar.get_width()
    mask = pygame.image.load('assets/pictures/adventure/进度条遮挡.png')
    flag=0
    flag2=0
    for i in range(0, TILESIZE, 1):
        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(emptyBar, (pygame.display.Info().current_w / 2 - emptyBar.get_width() / 2,pygame.display.Info().current_h - emptyBar.get_height()))
        fullBar = pygame.image.load('assets/pictures/adventure/进度条满.png')
        fullBar = pygame.transform.scale(fullBar, (i, fullBar.get_height()))

        SCREEN.blit(fullBar, (pygame.display.Info().current_w / 2 -TILESIZE/2, pygame.display.Info().current_h - fullBar.get_height()-23))
        SCREEN.blit(atk2, (pygame.display.Info().current_w / 2 - TILESIZE / 2 - 35 + i,
                           pygame.display.Info().current_h - atk2.get_height() - 12))

        SCREEN.blit(girla, (pygame.display.Info().current_w / 2 - TILESIZE / 2 - 20 + i,
                            pygame.display.Info().current_h - girla.get_height() - 15))
        SCREEN.blit(atk, (pygame.display.Info().current_w / 2 - TILESIZE / 2 - 35 + i,
                          pygame.display.Info().current_h - atk.get_height() - 12))



        flag += 1
        flag2+=1
        if flag == 20:
            girla = pygame.image.load('assets/pictures/adventure/图层 4.png')
        if flag == 40:
            girla = pygame.image.load('assets/pictures/adventure/图层 5.png')
        if flag == 60:
            girla = pygame.image.load('assets/pictures/adventure/图层 6.png')
            flag = 0


        if flag2 == 5:
            atk = pygame.image.load('assets/pictures/adventure/图层 13.png')#f
            atk2 = pygame.image.load('assets/pictures/adventure/图层 17.png')#b
        if flag2 == 10:
            atk = pygame.image.load('assets/pictures/adventure/图层 12.png')#f
            atk2 = pygame.image.load('assets/pictures/adventure/图层 18.png')#b
        if flag2 == 15:
            atk = pygame.image.load('assets/pictures/adventure/图层 9.png')#f
            atk2 = pygame.image.load('assets/pictures/adventure/图层 15.png')#b
        if flag2 == 20:
            atk = pygame.image.load('assets/pictures/adventure/图层 7.png')#f
            atk2 = pygame.image.load('assets/pictures/adventure/图层 16.png')#b
            flag2 = 0



        SCREEN.blit(mask, (pygame.display.Info().current_w / 2 - emptyBar.get_width() / 2 - mask.get_width()/2,pygame.display.Info().current_h - mask.get_height()*1.25))
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    print(TILESIZE)
