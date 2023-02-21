from moviepy.editor import *
import threading
import pygame, sys
from button import Button
import processBar



pygame.init()
SCREEN = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.FULLSCREEN)
pygame.display.set_caption("Menu")
BG = pygame.image.load("assets/Background.png")
BG = pygame.transform.scale(BG, (pygame.display.Info().current_w, pygame.display.Info().current_h))



def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)
def play():
    from ModelSelection import gameDifficulty
    gameDifficulty()
def main_menu():
    flag_sound1 = False
    flag_sound2 = False
    flag_sound3 = False
    flag_sound4 = False
    pygame.mixer.music.load("assets/music/bgm/menu_bgm.mp3")
    pygame.mixer.music.play(-1)
    # lower the volume of the music
    pygame.mixer.music.set_volume(1)
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("THINK TWICE", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN.get_width() / 2, SCREEN.get_height() *1/ 8))
        PLAY_BUTTON = Button(image=None, pos=(SCREEN.get_width() / 2, SCREEN.get_height()*5/ 16),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        ONLINE_BUTTON = Button(image=None, pos=(SCREEN.get_width() / 2, SCREEN.get_height()*21 / 32 ),
                               text_input="ONLINE", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(SCREEN.get_width() / 2, SCREEN.get_height()*13 / 16 ),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        ADVENTURE_BUTTON = Button(image=None, pos=(SCREEN.get_width() / 2, SCREEN.get_height()*15/ 32),
                                text_input="ADVENTURE", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        if flag_sound1 == False and PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
            pygame.mixer.Sound("assets/music/sound effect/bt_menu_click.mp3").play()
            flag_sound1 = True
        # mouse not hovering over the play button, sound effect will not play
        if flag_sound1 == True and not PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
            flag_sound1 = False

        if flag_sound2 == False and ONLINE_BUTTON.checkForInput(MENU_MOUSE_POS):
            pygame.mixer.Sound("assets/music/sound effect/bt_menu_click.mp3").play()
            flag_sound2 = True
        # mouse not hovering over the play button, sound effect will not play
        if flag_sound2 == True and not ONLINE_BUTTON.checkForInput(MENU_MOUSE_POS):
            flag_sound2 = False

        if flag_sound3 == False and QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
            pygame.mixer.Sound("assets/music/sound effect/bt_menu_click.mp3").play()
            flag_sound3 = True
        # mouse not hovering over the play button, sound effect will not play
        if flag_sound3 == True and not QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
            flag_sound3 = False

        if flag_sound4 == False and ADVENTURE_BUTTON.checkForInput(MENU_MOUSE_POS):
            pygame.mixer.Sound("assets/music/sound effect/bt_menu_click.mp3").play()
            flag_sound4 = True
        # mouse not hovering over the play button, sound effect will not play
        if flag_sound4 == True and not ADVENTURE_BUTTON.checkForInput(MENU_MOUSE_POS):
            flag_sound4 = False
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        for button in [PLAY_BUTTON, ONLINE_BUTTON, QUIT_BUTTON,ADVENTURE_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound("assets/music/sound effect/bt_tile_click.mp3").play()
                    pygame.mixer.music.load("assets/music/bgm/mode_1_summer.mp3")
                    pygame.mixer.music.play(-1)
                    play()
                if ONLINE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound("assets/music/sound effect/bt_tile_click.mp3").play()
                    pygame.mixer.music.load("assets/music/bgm/mode_4_fight.mp3")
                    pygame.mixer.music.play(-1)
                    from puzzleClient import puzzleClient
                    puzzleClient()
                if ADVENTURE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound("assets/music/sound effect/bt_tile_click.mp3").play()
                    pygame.mixer.music.load("assets/music/bgm/mode_3_desert.mp3")
                    pygame.mixer.music.play(-1)
                    t = threading.Thread(target=processBar.processbarAnimation)
                    t.start()
                    t.join()
                    from adventureModel import adventureModel
                    adventureModel()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound("assets/music/sound effect/bt_tile_click.mp3").play()
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


def loadVideo():
    cygames = VideoFileClip(r'assets/video/开头.mp4')
    cygames = cygames.resize((pygame.display.Info().current_w, pygame.display.Info().current_h))
    cygames.preview()
    cygames.close()


if __name__ == '__main__':
    loadVideo()
    main_menu()



