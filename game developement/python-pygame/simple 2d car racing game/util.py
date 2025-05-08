import pygame

def scale_image(img,factor):
    """this funtion is used to scale the img to a flavoured scale

    Args:
        img (file path): the targeted img
        factor (int): this will be multipied by the img's coordinate to scale it

    Returns:
        scaled version of the img    
    """
    size = round(img.get_width()*factor),round(img.get_height()*factor)
    return pygame.transform.scale(img,size)

def blit_rotate_centre(win,img,top_left,angle):
    """basicly this function rotates the img as if we do that manualy this 
    will cause undesired result making the img looks corrupted as the manual 
    rotation make a dispalcement(إزاحة) causing the img's pos to change

    Args:
        win (pygame.display): the window(img) of which the img is drawn
        img (file path): the desired img
        top_left (bool): 
        angle (num): _description_
    """
    rotated_img =pygame.transform.rotate(img,angle)
# this line is helps in stablizing the img's position while rotating
    new_rect = rotated_img.get_rect(center=img.get_rect(topleft = top_left).center)
    win.blit(rotated_img,new_rect.topleft)
    
