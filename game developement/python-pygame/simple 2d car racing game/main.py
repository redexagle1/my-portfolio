#region imports
import pygame
import time
# the custom hand-made function module
from util import scale_image,blit_rotate_centre
from game_class import *
import os
from dotenv import load_dotenv
# you know that paths are TOP SECRETS (IDK but incease)
load_dotenv('credintials.env')
file_path =os.getenv('my_path')
computer_path = []
#endregion 
#region assets
# idenefying the game's assets
TRACK = scale_image(pygame.image.load("C:/Users/saad/Documents/saad/my portofolio/my-portfolio/game developement/python-pygame/simple 2d car racing game/imgs/track.png"),.9)
GRASS = scale_image(pygame.image.load("C:/Users/saad/Documents/saad/my portofolio/my-portfolio/game developement/python-pygame/simple 2d car racing game/imgs/grass.jpg"),2.5)
FINISH = (pygame.image.load("C:/Users/saad/Documents/saad/my portofolio/my-portfolio/game developement/python-pygame/simple 2d car racing game/imgs/finish.png"))
FINISH_POSITION = (130,250)
FINISH_MASK = pygame.mask.from_surface(FINISH)
CAR_PLAYER = scale_image(pygame.image.load("C:/Users/saad/Documents/saad/my portofolio/my-portfolio/game developement/python-pygame/simple 2d car racing game/imgs/red-car.png"),.55)
CAR_ENEMY = scale_image(pygame.image.load("C:/Users/saad/Documents/saad/my portofolio/my-portfolio/game developement/python-pygame/simple 2d car racing game/imgs/green-car.png"),.55)
TRACK_BORDERS = scale_image(pygame.image.load("C:/Users/saad/Documents/saad/my portofolio/my-portfolio/game developement/python-pygame/simple 2d car racing game/imgs/track-border.png"),.9)
"""MASK its something we usr to make collusion in the pixel world
see,normal the image of your object wether contains pixel or transperancy background
python deals with it as a rectangle
so to seprate the transperancy background pixel(بكسلات الخلفيه الشفافه) from
the ones that actually contains pixel you need to use the mask
as it act as a 2d-matrix that store 1s,0s
as like this
    [
        [1,0,1,1,0]
        [1,0,0,0,0]
        [0,0,1,1,0]
    ]
    which 1 denotes that there is a pixel
    0 denotes that there is not a pixel
this helps us idenifying wether a 2 images collided or not
by a princible called the \\OFFSET(ازاحه)\\ 
we need to know the diffrences between the 2 images'top_left_hand coordinate to
determain wether the 2 images collided or no
so in a nutshell we will get the dislacement of 2 top_left_hand coordinate
to align the 2 image proberly before collidig them

to do that
1. make a mask_collusion function in the AbstractCar class
2. make condition to check if there is a P.O.I(Point Of Intersection)
3. make a bounce function in the PlayerCar class that perform the collusion process
    """
TRACK_BORDERS_MASK = pygame.mask.from_surface(TRACK_BORDERS)

#the list is for storing images to be drawn later in the while loop
images = [(GRASS,(0,0)),(TRACK,(0,0)),(FINISH,FINISH_POSITION),(TRACK_BORDERS,(0,0))]
player_car = CarPlayer(4,4,CAR_PLAYER)
comp_path=[(171, 159), (160, 88), (104, 84), (59, 119), (54, 195), (63, 371), (57, 474), (84, 510), (133, 546), (281, 687), (308, 716), (369, 729), (397, 693), (407, 636), (427, 504), (496, 487), (567, 495), (599, 575), (609, 690), (716, 720), (751, 615), (754, 545), (736, 414), (693, 358), (582, 355), (465, 358), (413, 303), (424, 267), (491, 256), (612, 254), (736, 233), (742, 145), (667, 75), (556, 77), (433, 76), (283, 98), (274, 194), (273, 264), (272, 324), (274, 383), (233, 409), (177, 393), (175, 316), (171, 260)]
computer_car = CarRobot(3,4,CAR_ENEMY,path = comp_path)

# setting up the screen
HEIGHT,WIDTH =TRACK_BORDERS.get_height(),TRACK_BORDERS.get_width()
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("racing game".title())
#endregion assets

#region FPS\render
"""those 2 is meant for controlling the rendering speed
uniting the renderd FPS so it runs on the same speed in any computer"""
'''this is for displayin them'''
def screen_drawing(win,imgs,player_car,computer_car):
    """rendering the drawings
    the blit(img,(x,y)) function draws the img in the specified coordinates
        NOTE that the coordinate vars works as the following
        the (x,y)(the topleft hand coordinate) consider as the origin piont 
        or in a better term the start piont then the program start from it
        and stretch till it reach the maximum size of the img  
    """
    '''this function will auto draw the imgs'''
    for img,pos in imgs:
        win.blit(img,pos)
    player_car.draw_car(win)
    computer_car.draw_car(win)
    #this will update the screen whenever we draw on it
    pygame.display.update()
FPS = 60
clock = pygame.time.Clock()
#endregion FPS
#region key controls 
def movement(player):
    # getting the user input
    keys = pygame.key.get_pressed()
    # the move switch
    moved = False
    # rotating the car
    if keys[pygame.K_LEFT]:player.rotate(left=True)
    elif keys[pygame.K_RIGHT]:player.rotate(right=True)
    #moving the car
    elif keys[pygame.K_UP]:
        player.moveforward()
        moved=True
    elif keys[pygame.K_DOWN]:
        player.movebackward()
        moved=True
    elif not moved:player.reduce_speed() # to apply the القصور الذاتي impact
#endregion key controls
# region loop
# initialize run to act as a switch
run = True
while run:
    """game logic is here(handling collusion,events)"""
    #region controlling/updating/setting FPS
    clock.tick(FPS) # this will make the loop cant run faster than 60FPS
    # rendring the imgs
    screen_drawing(WIN,images,player_car,computer_car)
    # controlling the movement
    movement(player_car)
    computer_car.move()
    # region collusion checks
    # check track collusion
    if player_car.collide(TRACK_BORDERS_MASK) != None:
        player_car.bounce()
    # check finish line collusion
    computer_finish_line_collusion =computer_car.collide(FINISH_MASK,*FINISH_POSITION)
    if computer_finish_line_collusion !=None:
        if computer_finish_line_collusion[1]==0:
            computer_car.bounce(True)
        else:
            player_car.reset()
            computer_car.reset()
            print("comp finish")       
    player_finish_line_collusion =player_car.collide(FINISH_MASK,*FINISH_POSITION)
    if player_finish_line_collusion !=None:
        if player_finish_line_collusion[1]==0:
            player_car.bounce(True)
        else:
            computer_car.reset()
            player_car.reset()
            print("finish")       
    # endregion collusion checks
    #endregion updating/setting FPS
    for event in pygame.event.get(): 
        """getting the user input 
        and checking if the user hit exit to break this loop"""
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     pos = pygame.mouse.get_pos()
        #     computer_car.path.append(pos)
        if event.type == pygame.QUIT:
            run =False
# print(computer_car.path)
# endregion loop
pygame.quit()      #end the program