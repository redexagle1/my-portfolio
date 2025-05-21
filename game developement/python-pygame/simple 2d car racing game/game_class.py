import pygame
import math
from util import blit_rotate_centre
#region classes
#region ABSTRACT car
class AbstractCar:
    def __init__(self,max_vel,rotation_vel,IMG):
        '''the constractor'''
        self.img = IMG
        self.max_vel = max_vel # max velocity
        self.rotation_vel = rotation_vel #rotation velocity
        self.vel =0 # velocity(the speed of the car)
        self.angel = 0
        self.x,self.y = self.START_POS #these are the origin pos(topleft pos)
        self.accelaration = .1 #يهتم بتسارع العربه مع الزمن
    def rotate(self,left=False,right = False):
        '''roate the car'''
        if left :
            self.angel += self.rotation_vel 
        elif right:
            self.angel -= self.rotation_vel 
    def moveforward(self):
        '''to move forward only'''
        self.vel =min(self.vel + self.accelaration,self.max_vel)
        self.move()
    def movebackward(self):
        '''to move backwards only'''
        #it will move back by the half of the max_velosity
        self.vel =max(self.vel - self.accelaration,-self.max_vel/2)
        self.move()
    def move(self):
        # self.x += self.vel      this alone will make the car move in 1 dimentional direction
        '''to move in the 2 dimrntional direction
        consider dealing with x,y trigonomitrcly,since velocity is associated
        with the x,y position of the car you need to draw it and identifying the 
        sin/cos/tan and based of *tech with tim racing car video(https://youtu.be/L3ktUWfAMPg?feature=shared&t=2663)*
        
        y = vel*sin(o) and x =vel*cos(o) : o represent the angle of the car
                                             measured by radians
        '''
        radians = math.radians(self.angel)
        vetical = self.vel * math.sin(radians)
        horizontical = self.vel * math.cos(radians)
        self.x -=vetical
        self.y -=  horizontical
    def draw_car(self,win):
        '''draw the CAR'''
        blit_rotate_centre(win,self.img,(self.x,self.y),self.angel)
    def collide(self,mask,x=0,y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x-x),int(self.y-y))
        '''#overlap :
        # بلبلدي بتقارن بين ازاحة الاتنين و لو حصل تداخل بينهم بطلع رقم غير كده
        # هطلع none'''
        poi = mask.overlap(car_mask,offset)
        return poi
    def reset(self):
        self.vel =0 # velocity(the speed of the car)
        self.angel = 0
        self.x,self.y = self.START_POS
# endregion ABSTRACT car
#region PLAYER car
class CarPlayer(AbstractCar):
    START_POS =(180,200)
    def __init__(self, max_vel, rotation_vel, IMG):
        super().__init__(max_vel, rotation_vel, IMG)
        self.isstop = False
    def movebackward(self):
        if self.isstop:
            return
        else: 
            super().movebackward()
    def moveforward(self):
        super().moveforward()
        self.stop(False)
    def reduce_speed(self):
        '''reduce the speed of the car by half of the accelarstion'''
        self.vel = max(self.vel-self.accelaration/2,0)
        self.move() 
    def bounce(self,block = False):
        if block:
            self.vel = 0
            self.stop(True)
        else:
            self.vel = -max(self.vel-self.accelaration/2,0)
            self.move()
    def stop(self,must_stop=False):
        if must_stop:
            self.isstop=True
        elif not(must_stop):
            self.isstop=False
class CarRobot(AbstractCar):
    START_POS =(150,200)
    def __init__(self, max_vel, rotation_vel, IMG, path =[]):
        super().__init__(max_vel, rotation_vel, IMG)
        self.path = path
        self.current_point = 0
        self.vel =max_vel 
    def move(self):
        if self.current_point >= len(self.path):
            ''' this if here to prvents an 
        index error if we tried to move to a point that doesn't exist'''
            return
        self.angel_calculation() 
        self.update_path() 
        ''' calculate the bot's angle and shifts toward that direction
        see if if the bot needs to move to a new point whenever the 
        bot hit a new point the''' 
        super().move()
    def angel_calculation(self):
        """this will calculate the angel which we need to 
        move to the next point
        """
        target_x,target_y = self.path[self.current_point]
        #differance calculation
        diff_x = target_x - self.x
        diff_y = target_y - self.y
        '''this condition check if diff_y = 0 
        if so the angle will be 90 by radian
        if not it will get the differance of y and x devide them to get arctan()
        this will lead us to calculate which direction the car is and will help in
        changing the bot's direction smoothly'''
        
        if diff_y == 0 :
            desired_radian_angle = math.pi/2 
        else:
            desired_radian_angle=math.atan(diff_x/diff_y)
        
        """this condition is responsible of fixxing the angle slightly
        you se we are calculating the acute(less than 90 degrees)angle but if the 
        diffrence between our target and our calculated angle is huge this will 
        results an extreme turning which is unwanted so by adding PI to our angle
        we reverse the turning direction
        """
        if target_y > self.y:
            desired_radian_angle += math.pi
        differance_in_angel = self.angel - math.degrees(desired_radian_angle)
        
        
        """so this code block checks if our difference in angle > 180 since if 
        that happen your bot will turn in a wrong direction unsmoothly so by 
        subtacting 360 we will make the car rotate smoothly in the correct direction 
        """
        if differance_in_angel >= 180:
            differance_in_angel -= 360
            # print('PATH UPDATED')
            
        """this code block snap on the desired angle smoothly as if we depend on 
        one of them the rotation will be unaccurate
        """
        if differance_in_angel >0:
            self.angel -= min(self.rotation_vel,abs(differance_in_angel))
        else:
            self.angel += min(self.rotation_vel,abs(differance_in_angel))
        """YEP ANGLES ARE DIFFICULT"""
    
    def update_path(self):
        """move to the next point of our path list"""
        target = self.path[self.current_point]
        rect =  pygame.Rect(self.x,self.y,self.img.get_width(),self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1    
            
    def draw_point(self,win):
        for points in self.path:
            pygame.draw.circle(win,(255,0,0),points,5)
    
    def draw_car(self, win):
        super().draw_car(win)
        # self.draw_point(win)
#endregion PLAYER car
#endregion classes   