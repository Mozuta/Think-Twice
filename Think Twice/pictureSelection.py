#加载所有assets/pictures目录下的图片
import pygame,sys,os
from button import Button
from exp import picselect
import puzzle

pygame.init()
#gamePictures difficulty selection
SCREEN = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.FULLSCREEN)
BG = pygame.image.load("assets/pictures/background/pictureSelection.png")
#change BG size fo full screen
BG = pygame.transform.scale(BG, (pygame.display.Info().current_w, pygame.display.Info().current_h))


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)
def load_images():
    images = {}
    #load all images in assets/pictures
    for file in os.listdir("assets/pictures/puzzle"):
        # load all images in assets/pictures
        if file.endswith(".jpg") or file.endswith(".png"):
            #fix the image size
            image = pygame.image.load("assets/pictures/puzzle/" + file)
            image = pygame.transform.scale(image, (500, 500))
            images[file] = image
    return images


#用户滚动选择图片开始游戏
def picture_selection():
    flag_sound1 = False
    flag_sound2 = False
    flag_sound3 = False
    flag_sound4 = False
    flag_sound5= False
    from main import main_menu
    images = load_images()
    image_names = list(images.keys())
    image_index = 0
    while True:
        SCREEN.blit(BG, (0, 0))
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_BACK = Button(image=None, pos=(SCREEN.get_width() *4/ 5, SCREEN.get_height()*14/15),
                            text_input="BACK", font=get_font(50), base_color="White", hovering_color="Green")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        OPTIONS_NEXT = Button(image=None, pos=(SCREEN.get_width() *5/6, 700),
                            text_input="NEXT", font=get_font(50), base_color="White", hovering_color="Green")
        OPTIONS_NEXT.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_NEXT.update(SCREEN)
        OPTIONS_PREVIOUS = Button(image=None, pos=(SCREEN.get_width() /6, 700),
                            text_input="LAST", font=get_font(50), base_color="White", hovering_color="Green")
        OPTIONS_PREVIOUS.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_PREVIOUS.update(SCREEN)
        OPTIONS_START = Button(image=None, pos=(SCREEN.get_width() / 2, 700),
                            text_input="START", font=get_font(100), base_color="White", hovering_color="Green")
        OPTIONS_START.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_START.update(SCREEN)
        # 用户导入图片
        OPTIONS_IMPORT = Button(image=None, pos=(SCREEN.get_width() / 5, SCREEN.get_height()*14/15),
                                text_input="IMPORT", font=get_font(50), base_color="White", hovering_color="Green")
        OPTIONS_IMPORT.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_IMPORT.update(SCREEN)
        #最左侧划分一片黑色区域
        #pygame.draw.rect(SCREEN, (0, 0, 0), (0, 0, 300, 400))
        #在此屏幕中间内显示图片
        SCREEN.blit(images[image_names[image_index]], (SCREEN.get_width() *36/ 100, SCREEN.get_height()/15))
        if flag_sound1 == False and OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
            pygame.mixer.Sound("assets/music/sound effect/bt_menu_click.mp3").play()
            flag_sound1 = True
        # mouse not hovering over the play button, sound effect will not play
        if flag_sound1 == True and not OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
            flag_sound1 = False

        if flag_sound2 == False and OPTIONS_START.checkForInput(OPTIONS_MOUSE_POS):
            pygame.mixer.Sound("assets/music/sound effect/bt_menu_click.mp3").play()
            flag_sound2 = True
        # mouse not hovering over the play button, sound effect will not play
        if flag_sound2 == True and not OPTIONS_START.checkForInput(OPTIONS_MOUSE_POS):
            flag_sound2 = False

        if flag_sound3 == False and OPTIONS_PREVIOUS.checkForInput(OPTIONS_MOUSE_POS):
            pygame.mixer.Sound("assets/music/sound effect/bt_menu_click.mp3").play()
            flag_sound3 = True
        # mouse not hovering over the play button, sound effect will not play
        if flag_sound3 == True and not OPTIONS_PREVIOUS.checkForInput(OPTIONS_MOUSE_POS):
            flag_sound3 = False

        if flag_sound4 == False and OPTIONS_NEXT.checkForInput(OPTIONS_MOUSE_POS):
            pygame.mixer.Sound("assets/music/sound effect/bt_menu_click.mp3").play()
            flag_sound4 = True
        # mouse not hovering over the play button, sound effect will not play
        if flag_sound4 == True and not OPTIONS_NEXT.checkForInput(OPTIONS_MOUSE_POS):
            flag_sound4 = False

        if flag_sound5 == False and OPTIONS_IMPORT.checkForInput(OPTIONS_MOUSE_POS):
            pygame.mixer.Sound("assets/music/sound effect/bt_menu_click.mp3").play()
            flag_sound5 = True
        # mouse not hovering over the play button, sound effect will not play
        if flag_sound5 == True and not OPTIONS_IMPORT.checkForInput(OPTIONS_MOUSE_POS):
            flag_sound5 = False



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if OPTIONS_NEXT.checkForInput(OPTIONS_MOUSE_POS):
                    image_index = (image_index + 1) % len(image_names)
                if OPTIONS_PREVIOUS.checkForInput(OPTIONS_MOUSE_POS):
                    image_index = (image_index - 1) % len(image_names)
                if OPTIONS_IMPORT.checkForInput(OPTIONS_MOUSE_POS):
                    picselect()
                    images = load_images()
                    image_names = list(images.keys())
                    image_index = 0
                if OPTIONS_START.checkForInput(OPTIONS_MOUSE_POS):
                    #puzzle.getImage(images[image_names[image_index]])
                    puzzle.IMAGEPATH = "assets/pictures/puzzle/" + image_names[image_index]
                    puzzle.IMAGES = []
                    puzzle.allMoves = []
                    puzzle.STEPS = 0
                    puzzle.main()
        pygame.display.update()





if __name__ == "__main__":
    picture_selection()








