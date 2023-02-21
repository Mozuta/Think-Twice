import pygame,sys
from button import Button
import puzzle
import pictureSelection

pygame.init()
#gamePictures difficulty selection
SCREEN = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h),pygame.FULLSCREEN,32)
BG = pygame.image.load("assets/pictures/background/ModelSelection.png")
#change BG size fo full screen
BG = pygame.transform.scale(BG, (pygame.display.Info().current_w, pygame.display.Info().current_h))





def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)
def gameDifficulty():
    flag_sound1 = False
    flag_sound2 = False
    flag_sound3 = False
    flag_sound4 = False
    flag_sound5 = False
    flag_sound6 = False
    pygame.display.update()
    from main import main_menu
    text_input = pygame.Rect(SCREEN.get_width() *6/15-100, SCREEN.get_height()/5+400, 140, 32)

    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('red')

    # 文本输入框颜色
    color = color_inactive
    # 文本输入框激活状态
    active = False
    # 文本输入框内容
    text = ''
    # 文本输入框字体黑色
    font = pygame.font.Font(None, 32)

    pygame.display.update()
    OPTIONS_NUM = Button(image=None, pos=(SCREEN.get_width() * 8.65 / 15, SCREEN.get_height() / 5 + 50),
                         text_input=" ", font=get_font(75), base_color="White", hovering_color="Green")
    while True:
        #BG
        SCREEN.blit(BG, (0, 0))
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_MOUSE_CLICK = pygame.mouse.get_pressed()

        OPTIONS_BACK = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(SCREEN.get_width() *11/15, SCREEN.get_height()/5+110),
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        #Button to change the 3x3, 4x4, 5x5 in puzzle.py
        OPTIONS_3x3 = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(SCREEN.get_width() *6/15, SCREEN.get_height()/5),
                            text_input='3x3', font=get_font(75), base_color="White", hovering_color="Green")
        OPTIONS_4x4 = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(SCREEN.get_width() *6/15, SCREEN.get_height()/5+110),
                            text_input="4x4", font=get_font(75), base_color="White", hovering_color="Green")
        OPTIONS_5x5 = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(SCREEN.get_width() *6/15, SCREEN.get_height()/5+220),
                            text_input="5x5", font=get_font(75), base_color="White", hovering_color="Green")
        #nxn
        OPTIONS_nxn = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(SCREEN.get_width() *6/15, SCREEN.get_height()/5+330),
                            text_input="NxN", font=get_font(75), base_color="White", hovering_color="Green")
        #文本输入框
        #排行榜
        OPTIONS_honor = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(SCREEN.get_width() *11/15, SCREEN.get_height()/5+330),
                            text_input="Rank", font=get_font(75), base_color="White", hovering_color="Green")
        OPTIONS_nxn.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_nxn.update(SCREEN)
        OPTIONS_BACK.changeText(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        #OPTIONS_NUM.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_NUM.update(SCREEN)
        OPTIONS_3x3.changeColor(OPTIONS_MOUSE_POS)#####

        OPTIONS_3x3.update(SCREEN)
        OPTIONS_4x4.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_4x4.update(SCREEN)
        OPTIONS_5x5.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_5x5.update(SCREEN)
        OPTIONS_honor.changeText(OPTIONS_MOUSE_POS)
        OPTIONS_honor.update(SCREEN)

        if flag_sound1 == False and OPTIONS_3x3.checkForInput(OPTIONS_MOUSE_POS):
            pygame.mixer.Sound("assets/music/sound effect/bt_menu_click.mp3").play()
            flag_sound1 = True
        # mouse not hovering over the play button, sound effect will not play
        if flag_sound1 == True and not OPTIONS_3x3.checkForInput(OPTIONS_MOUSE_POS):
            flag_sound1 = False

        if flag_sound2 == False and OPTIONS_4x4.checkForInput(OPTIONS_MOUSE_POS):
            pygame.mixer.Sound("assets/music/sound effect/bt_menu_click.mp3").play()
            flag_sound2 = True
        # mouse not hovering over the play button, sound effect will not play
        if flag_sound2 == True and not OPTIONS_4x4.checkForInput(OPTIONS_MOUSE_POS):
            flag_sound2 = False

        if flag_sound3 == False and OPTIONS_5x5.checkForInput(OPTIONS_MOUSE_POS):
            pygame.mixer.Sound("assets/music/sound effect/bt_menu_click.mp3").play()
            flag_sound3 = True
        # mouse not hovering over the play button, sound effect will not play
        if flag_sound3 == True and not OPTIONS_5x5.checkForInput(OPTIONS_MOUSE_POS):
            flag_sound3 = False

        if flag_sound4 == False and OPTIONS_nxn.checkForInput(OPTIONS_MOUSE_POS):
            pygame.mixer.Sound("assets/music/sound effect/bt_menu_click.mp3").play()
            flag_sound4 = True
        # mouse not hovering over the play button, sound effect will not play
        if flag_sound4 == True and not OPTIONS_nxn.checkForInput(OPTIONS_MOUSE_POS):
            flag_sound4 = False

        if flag_sound5 == False and OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
            pygame.mixer.Sound("assets/music/sound effect/bt_menu_click.mp3").play()
            flag_sound5 = True
        # mouse not hovering over the play button, sound effect will not play
        if flag_sound5 == True and not OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
            flag_sound5 = False

        if flag_sound6 == False and OPTIONS_honor.checkForInput(OPTIONS_MOUSE_POS):
            pygame.mixer.Sound("assets/music/sound effect/bt_menu_click.mp3").play()
            flag_sound6 = True
        # mouse not hovering over the play button, sound effect will not play
        if flag_sound6 == True and not OPTIONS_honor.checkForInput(OPTIONS_MOUSE_POS):
            flag_sound6 = False





        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    #return to main menu
                    pygame.mixer.Sound("assets/music/sound effect/bt_tile_click.mp3").play()
                    main_menu()
                if OPTIONS_3x3.checkForInput(OPTIONS_MOUSE_POS):
                    #change the BOARDWIDTH in puzzle.py to 3 and then go back to main menu
                    puzzle.BOARDWIDTH = 3
                    puzzle.BOARDHEIGHT = 3
                    puzzle.PATTERN = 2
                    puzzle.TILESIZE = 250
                    pygame.mixer.Sound("assets/music/sound effect/bt_tile_click.mp3").play()
                    #puzzle.main()
                    pictureSelection.picture_selection()

                if OPTIONS_4x4.checkForInput(OPTIONS_MOUSE_POS):
                    #change the BOARDWIDTH in puzzle.py to 4
                    puzzle.BOARDWIDTH = 4
                    puzzle.BOARDHEIGHT = 4
                    puzzle.PATTERN = 2
                    puzzle.TILESIZE = int(750 / 4)
                    pygame.mixer.Sound("assets/music/sound effect/bt_tile_click.mp3").play()
                    pictureSelection.picture_selection()
                if OPTIONS_5x5.checkForInput(OPTIONS_MOUSE_POS):
                    #change the BOARDWIDTH in puzzle.py to 5
                    puzzle.BOARDWIDTH = 5
                    puzzle.BOARDHEIGHT = 5
                    puzzle.PATTERN = 2
                    puzzle.TILESIZE = int(750 / 5)
                    pygame.mixer.Sound("assets/music/sound effect/bt_tile_click.mp3").play()
                    pictureSelection.picture_selection()
                if OPTIONS_NUM.checkForInput(OPTIONS_MOUSE_POS):
                    print(OPTIONS_NUM.text_input)
                    #change the BOARDWIDTH in puzzle.py to 5
                    OPTIONS_NUM.changenum()
                    print(OPTIONS_NUM.text_input)
                    OPTIONS_NUM.update(SCREEN)



                if OPTIONS_nxn.checkForInput(OPTIONS_MOUSE_POS):
                    active = not active
                if OPTIONS_honor.checkForInput(OPTIONS_MOUSE_POS):
                    pygame.mixer.Sound("assets/music/sound effect/bt_tile_click.mp3").play()
                    from Models.Rank import showRank
                    showRank()

            #文本输入框
            if event.type == pygame.MOUSEBUTTONUP:
                # If the user clicked on the input_box rect.
                if text_input.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                # Change the current color of the input box.
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    #只接收number
                    if event.key == pygame.K_RETURN:
                        for i in range(6,11):
                            if(text.isdecimal()):
                                if(int(text)==i):
                                    print(text)
                                    puzzle.BOARDWIDTH = int(text)
                                    puzzle.BOARDHEIGHT = int(text)
                                    puzzle.TILESIZE = int(750 / int(text))
                                    puzzle.PATTERN = 2
                                    pygame.mixer.Sound("assets/music/sound effect/bt_tile_click.mp3").play()
                                    pictureSelection.picture_selection()
                                    text = ''

                            else:
                                pass



                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode







        txt_surface = font.render(text, True, (0, 255, 0))
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        text_input.w = width
        # Blit the text.
        SCREEN.blit(txt_surface, (text_input.x + 5, text_input.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(SCREEN, color, text_input, 2)








        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()





