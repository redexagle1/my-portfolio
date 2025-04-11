import pygame
from util import *
TRACK_BORDERS = scale_image(pygame.image.load("imgs/track-border.png"),.9)
TRACK_BORDERS_MASK = pygame.mask.from_surface(TRACK_BORDERS)
CAR_ENEMY = (pygame.image.load("imgs/green-car.png"))
MASKED = pygame.mask.from_surface(CAR_ENEMY)
