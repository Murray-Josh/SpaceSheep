import pygame
import physics
import math as maths
import ctypes
import random

# Takes the screen size of the users monitor and sets it as the display size
user32 = ctypes.windll.user32

# Defining background outside of game loop, as this can cause lag
background = pygame.image.load("background.jpg")


# Class for all constants that will be used throughout the program
class user:
        # Finds the size of users screen and saves as new variables
        displayWidth = user32.GetSystemMetrics(0)
        displayHeight = user32.GetSystemMetrics(1)
        screen = pygame.display.set_mode((displayWidth, displayHeight))

        # Variable to allow files to be accessed in separate folders
        images = "images\\"


# Class for moving objects
class moveobj:
    # Initiates the object through defining its angle, coordinates, speed and more
    def __init__(self, x, y, sp, a, s):
        self.x = x
        self.y = y
        self.angle = a
        self.speed = sp
        self.direction = 0
        self.size = s

        self.image = pygame.transform.smoothscale(self.image, (self.size, self.size))

    # Defines the rotation that will rotate an image according to the direction of the ship
    def rotate(self):
        self.rotimage = pygame.transform.rotate(self.image, self.direction * 57)

    # Method to blit the ship to the screen
    def display(self):
        user.screen.blit(self.rotimage, (self.x, self.y))

    def hitBox(self):
        pygame.draw.rect(user.screen, (000, 255, 000), (self.x, self.y , self.size, self.size))

    # Update function that brings together display, movement and rotating
    def update(self):
        moveobj.rotate(self)
        moveobj.display(self)


# Defines a ship class with inheritance from moving objects
class ship(moveobj):
    # Initiates ship using super and adding life
    def __init__(self, x, y, sp, l, s):
        super().__init__(x, y, sp, 0, s)
        self. life = 3
        self.score = 0

    # Method for the ships movement
    def move(self):
        # Variable to apply continues drag
        self.speed *= 0.999

        if self.speed > 5:
            self.speed = 5

        self.x += maths.sin(self.angle) * self.speed
        self.y -= maths.cos(self.angle) * self.speed

    def update(self):
        super().update()
        ship.move(self)


# Defines a ship class with inheritance from ship
class playable(ship):
    # Initiates the playable class using ships update and adding ammo and new image
    def __init__(self, x, y, sp):
        self.image = pygame.image.load("ship.png").convert_alpha()
        super().__init__(x, y, 0, 20, 30)
        self.ammo = 10

    def ammoBar(self):
        pygame.draw.rect(user.screen, (111, 000, 255), (10, user.displayHeight - 40, self.ammo*10, 25))
    # Update function that brings together display, movement and rotating

    def healthBar(self):
        pygame.draw.rect(user.screen, (255, 000, 000), (10, user.displayHeight - 80, self.life*10, 25))
    # Update function that brings together display, movement and rotating

    def update(self):
        super().update()
        playable.ammoBar(self)
        playable.healthBar(self)


class enemy(ship):
    def __init__(self, x, y, sp):
        self.image = pygame.image.load("enemy.png").convert_alpha()
        super().__init__(x, y, sp, 10, 40)
        self.speed = -2
        self.life = 1

    def chase(self, user):
        spXChange = random.randint(-500, 500) / 100
        spYChange = random.randint(-500, 500) / 100
        if self.speed >= 0:
            self.speed = -2
        (eDis, eA) = physics.lenang(user.x, user.y, self.x + self.size / 4, self.y + self.size /4)
        dx, dy = self.x - user.x, self.y - user.y
        dx, dy = dx / eDis, dy / eDis

        self.x += dx * (spXChange + self.speed)
        self.y += dy * (spYChange + self.speed)
        super().rotate()
        super().display()


# Class for the firing with inheritance from movobj class
class fire(moveobj):

    # Runs the ship initialisation with the addition of a new image and life
    def __init__(self, x, y, a):
        self.image = pygame.image.load("fire.png").convert_alpha()
        super().__init__(x, y, 900, a, 5)
        self.life = 60

    def move(self):
        self.x += maths.sin(self.angle) * self.speed
        self.y -= maths.cos(self.angle) * self.speed

    #  Fills the image and blends colours to give an effect of transparenct representing disipation
    def alpha(self):
        alpha = 252
        self.image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)

    def update(self):
        fire.move(self)
        fire.rotate(self)
        fire.display(self)
        fire.alpha(self)
        # In each iteration of the main loop the bullet will lose a life so it will eventually die
        self.life -= 1


# Class for ammo box inheriting from moveobj class
class ammoBox(moveobj):
    def __init__(self, x, y):
        self.image = pygame.image.load("ammoBox.png").convert_alpha()

        super().__init__(x, y, 0, 0, 20)

        # Sets initial angle to be random
        self.direction = random.randrange(0, 180)

    # Method to make the box continuously spin
    def spin(self):
        self.direction += 0.05

    def update(self):
        ammoBox.spin(self)
        super().update()


class healthBox(moveobj):
    def __init__(self, x, y):
        self.image = pygame.image.load("healthBox.png").convert_alpha()

        super().__init__(x, y, 0, 0, 20)

        # Sets initial angle to be random
        self.direction = random.randrange(0, 180)

    # Method to make the box continuously spin
    def spin(self):
        self.direction += 0.05

    def update(self):
        healthBox.spin(self)
        super().update()


class dwayneTheRockJohnnson(moveobj):
    def __init__(self, x, y):
        self.image = pygame.image.load("rocks.png").convert_alpha()
        super().__init__(x, y, 0, 0, 200)

    def gPull(self, i):
            (rockDis, rockA) = physics.lenang(i.x, i.y, self.x + self.size/2, self.y + self.size/2)
            (i.angle, i.speed) = physics.addvectors(i.angle, i.speed, maths.pi - rockA, - (100 / (rockDis+self.size ** 2)))


