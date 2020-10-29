import math as maths
import pygame
import classes

pygame.init()


def addvectors(angle1, length1, angle2, length2):
    x = maths.sin(angle1) * length1 + maths.sin(angle2) * length2  # Defines x using trigonometry
    y = maths.cos(angle1) * length1 + maths.cos(angle2) * length2  # Defines Y using trigonometry
    angle = 0.5 * maths.pi - maths.atan2(y, x)  # Defines angle using trig atan = arctan
    length = maths.hypot(x, y)  # Sets the length of the vector, hypot = hypotenuse

    return angle, length  # Returns angle and length


# Function to take input of two objects and find angle and distance between them
def lenang(obj1X, obj1Y, obj2X, obj2Y):
    dx = obj1X - obj2X
    dy = obj1Y - obj2Y
    length = maths.hypot(dx, dy)
    angle = maths.atan2(dx, dy)
    return length, angle


font = pygame.font.SysFont("arial", 70, False, False)


def text(text, col):
    textSurf = font.render(text, True, col)
    return textSurf, textSurf.get_rect()


def message(msg,x,y, col):
    textSurf, textRect = text(msg, col)
    textRect.center = (x, y)
    classes.user.screen.blit(textSurf, textRect)

