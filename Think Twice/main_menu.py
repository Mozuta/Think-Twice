import pygame,sys

IMAGES = []

BOARDWIDTH = 3  # number of columns in the board
BOARDHEIGHT = 3
# load image and split it into 3*3 tiles and store in IMAGES
SCREEN = pygame.display.set_mode((800, 600))
def loadImages():
    # Load the image and convert it to have alpha.
    image = pygame.image.load('assets/pictures/p6.jpg')
    image = image.convert_alpha()

    # Calculate the width and height of each tile.
    imageWidth = int(image.get_width() / BOARDWIDTH)
    imageHeight = int(image.get_height() / BOARDHEIGHT)

    # Create each of the tiles.
    for tilex in range(BOARDWIDTH):
        for tiley in range(BOARDHEIGHT):
            left = tilex * imageWidth
            top = tiley * imageHeight
            tileImage = image.subsurface((left, top, imageWidth, imageHeight))
            IMAGES.append(tileImage)
#display IMAGES in 3*3 grid
def displayImages():
    x = 0
    y = 0
    for i in range(BOARDWIDTH * BOARDHEIGHT):
        SCREEN.blit(IMAGES[i], (x, y))
        x += 200
        if x == 600:
            x = 0
            y += 200


#main loop
def main():
    loadImages()
    while True:
        SCREEN.fill((0,0,0))
        displayImages()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
#main
if __name__ == '__main__':
    main()



