import pygame
import classes
import physics
import math as maths
import random
import noise
import time
from tkinter import *
import gui

# Defining background outside of game loop, as this can cause lag
background = pygame.image.load("background.jpg")

# Sets the FPS or clock speed of the program
clock = pygame.time.Clock()

# Sets user as a class of user for
users = classes.user

gameIcon = pygame.image.load('icon.png')
pygame.display.set_icon(gameIcon)


def maingame():
    mainLoop = True
    hitBoxes = False

    ##MUSIC##
    shotfx = pygame.mixer.Sound('ion.wav')
    shotfx.set_volume(0.2)
    pygame.mixer.music.load('spacesong.wav')
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)

    # Generates the users playable ship
    userShip = classes.playable(users.displayWidth / 2, users.displayHeight / 2, 0)

    # Creates list for storing of bullets
    bullets = []

    # Creates list for bullets and creates one
    boxes = [
        classes.ammoBox(random.randint(0 + 0, users.displayWidth + 0), random.randint(0 + 0, users.displayHeight + 0))]

    # Creates a list for health boxes
    hBoxes = []
    # Creates list for enemies and appends one
    enemies = [
    ]

    asteroids = [classes.dwayneTheRockJohnnson(random.randint(0 + 0, users.displayWidth + 0),
                                               random.randint(0 + 0, users.displayHeight + 0))
                 ]
    # Sets variables to be used later
    coolDown = 0
    direction = 0
    hitCoolDown = 0
    level = 0

    pygame.display.update()
    # Main game loop
    while mainLoop:

        # Cursor variable to be used later
        cursor = pygame.mouse.get_pos()

        # Blits the background to the screen
        users.screen.blit(background, (0, 0))

        # Gets the distance of mouse and angle from the ship
        (mouseDis, mouseA) = physics.lenang(userShip.x, userShip.y, cursor[0], cursor[1])

        # Variable to use for key presses
        keys = pygame.key.get_pressed()

        # Takes the ships current angle and direction and uses a function to add forward momentum
        if keys[pygame.K_w]:
            (userShip.angle, userShip.speed) = physics.addvectors(userShip.angle, userShip.speed,
                                                                  2 * maths.pi - (maths.pi / 2 + userShip.direction),
                                                                  -0.1)

        # Slow down key
        if keys[pygame.K_s]:
            userShip.speed *= 0.98

        # Rotates the ship to the left or right
        if keys[pygame.K_a]:
            userShip.direction += 0.05
            if direction >= 2 * maths.pi:
                direction = 0

        if keys[pygame.K_d]:
            userShip.direction -= 0.05
            # Allow the direction to loop when a full rotation is done to prevent out of range valuies
            if direction < 0:
                direction = 2 * maths.pi

        # Checks for shot with space key
        if keys[pygame.K_SPACE]:
            # Checks that the user has ammo and cool downed
            if coolDown <= 0 < userShip.ammo:
                shotfx.stop()
                shotfx.play()
                # Generates a shot and appends to the list
                shot = (
                classes.fire(userShip.x + 15, userShip.y + 15, (2 * maths.pi + (maths.pi / 2 - userShip.direction))))
                (shot.angle, shot.speed) = physics.addvectors(userShip.angle, userShip.speed, 2 * maths.pi - (
                        maths.pi / 2 + userShip.direction), -5)
                bullets.append(shot)

                # Sets a new cool down and removes 1 ammo
                coolDown = 5
                userShip.ammo -= 1

        # Key to set hitboxes on for debuging

        for event in pygame.event.get():
            # Event to deal with the exiting of the game screen
            if event.type == pygame.QUIT:
                mainLoop = False
                menuscreen = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainLoop = False
                    menuscreen = False

                if event.key == pygame.K_TAB:
                    if hitBoxes:
                        hitBoxes = False

                    else:
                        hitBoxes = True

        # Draws blue border around game window
        pygame.draw.rect(users.screen, (0, 0, 255), [0, 0, users.displayWidth, users.displayHeight], 6)

        # When the ship reacehs the border at a vector in the opposite direction to repel the ship
        if userShip.x <= 0:
            (userShip.angle, userShip.speed) = physics.addvectors(userShip.angle, userShip.speed, 0.5 * maths.pi, 2)

        if userShip.x + 36 >= users.displayWidth:
            (userShip.angle, userShip.speed) = physics.addvectors(userShip.angle, userShip.speed, -0.5 * maths.pi, 2)

        if userShip.y + 36 >= users.displayHeight:
            (userShip.angle, userShip.speed) = physics.addvectors(userShip.angle, userShip.speed, maths.pi, -2)

        if userShip.y <= 0:
            (userShip.angle, userShip.speed) = physics.addvectors(userShip.angle, userShip.speed, maths.pi, 2)

        # Iterates through and updates all bullets
        for o in bullets:
            o.update()
            # Removes the time remaining for bullet, then removes it from the list
            if o.life <= 0:
                bullets.remove(o)
            if hitBoxes:
                o.hitBox()
        hitCoolDown -= 1

        if len(enemies) < 1:
            if level == 0:
                physics.message("PRESS X TO START!", classes.user.displayWidth / 2, classes.user.displayHeight / 2,
                                (255, 255, 255))
                if keys[pygame.K_x]:
                    enemies.append(classes.enemy(random.randint(0 + 0, users.displayWidth + 0),
                                                 random.randint(0 + 0, users.displayHeight + 0), 0))
                    level += 1


            else:
                userShip.score += 10
                level += 1
                physics.message("Level: " + str(level), classes.user.displayWidth / 2, classes.user.displayHeight / 2,
                                (255, 255, 255))
                pygame.display.update()
                time.sleep(1)

                if level % 5 == 0:
                    asteroids.append(classes.dwayneTheRockJohnnson(random.randint(0, classes.user.displayWidth),
                                                                   random.randint(0, classes.user.displayHeight)))
                    hBoxes.append((classes.healthBox(random.randint(0 , users.displayWidth),
                                                     random.randint(0 , users.displayHeight))))
                print(hBoxes)
                for i in range(0, 2):
                    if len(boxes) < 4:
                        boxes.append(classes.ammoBox(random.randint(0 , users.displayWidth),
                                                     random.randint(0 , users.displayHeight)))
                for i in range(1, random.randint(1, level * 2)):
                    enemies.append(classes.enemy(random.randint(0, users.displayWidth),
                                                 random.randint(0, users.displayHeight), 0))

        # Iterates through every enemy and updates it
        for e in enemies:
            e.chase(userShip)
            # Checks distance between bullet and enemy to see if its hit
            for b in bullets:
                if physics.lenang(b.x + b.size / 2, b.y + b.size / 2, e.x + e.size / 2, e.y + e.size / 2)[0] <= (
                        e.size / 2 + b.size / 2):
                    e.life -= 1
                    bullets.remove(b)
                    userShip.score += 20

            if hitCoolDown <= 0:
                if physics.lenang(userShip.x + userShip.size / 2, userShip.y + userShip.size / 2, e.x + e.size / 2,
                                  e.y + e.size / 2)[0] <= (
                        e.size / 2 + userShip.size / 2):
                    (e.angle, e.speed) = physics.addvectors(e.angle, e.speed,
                                                            -0.5 * maths.pi, 2)
                    e.speed = -3
                    userShip.life -= 1
                    hitCoolDown = 60

            # If the user is dead removes it from the game
            if e.life <= 0:
                enemies.remove(e)

            if hitBoxes:
                e.hitBox()

        # Iterates through all ammo boxes and updates them
        for b in boxes:
            b.update()

            # Check ammo for contact with the user, if so add ammo to user
            if physics.lenang(userShip.x + 15, userShip.y + 15, b.x + 10, b.y + 10)[0] <= 25:
                boxes.remove(b)
                userShip.ammo += 10

            if hitBoxes:
                b.hitBox()

        for h in hBoxes:
            h.update()

            # Check ammo for contact with the user, if so add ammo to user
            if physics.lenang(userShip.x + 15, userShip.y + 15, h.x + 10, h.y + 10)[0] <= 25:
                hBoxes.remove(h)
                userShip.life += 20

        # Updates the ship and each object of a shot in the list
        userShip.update()

        if hitBoxes:
            userShip.hitBox()

        if userShip.life <= 0:
            mainLoop = False
            endGame(userShip.score)

        for a in asteroids:
            a.update()
            a.gPull(userShip)
            if hitCoolDown <= 0:
                if physics.lenang(userShip.x + userShip.size / 2, userShip.y + userShip.size / 2, a.x + a.size / 2,
                                  a.y + a.size / 2)[0] <= (
                        a.size / 2 + userShip.size / 2):
                    userShip.life -= 1
                    hitCoolDown = 60
            # for e in enemies:
            #    a.gPull(e)
            if hitBoxes:
                a.hitBox()

        userShip.score += 0.1 / 60
        physics.message("Score: " + str(round(userShip.score, 1)), classes.user.displayWidth / 2, 30, [255, 255, 255])
        # Cool down for bullet taken down one per tick
        coolDown -= 1

        # Updates the display and sets clock speed
        pygame.display.update()
        clock.tick(60)


def endGame(score):
    end = False
    physics.message("You Died", classes.user.displayWidth / 2, classes.user.displayHeight / 2 - 90, (255, 255, 255))
    physics.message("Tweet score (y)", classes.user.displayWidth * 1 / 3, classes.user.displayHeight / 2 + 200,
                    (255, 255, 255))
    physics.message("Quit (n)", classes.user.displayWidth * 2 / 3, classes.user.displayHeight / 2 + 200,
                    (255, 255, 255))
    text_file2 = open("score.txt", "w")
    text_file2.write(str(int(score)))
    text_file2.close()
    # text_file = open("HighScore.txt", "r")
    with open("HighScore.txt", 'r') as f:
        ret = []
        for line in f:
            ret += line.split()
    High = ret[0]
    #High = int(High)

    if int(High,0) < int(score):
        text_file = open("HighScore.txt", "w")
        text_file.write(str(int(score)))
        text_file.close()
        print("Highscore Saved")
        physics.message("Your New High Score is : " + str(score), classes.user.displayWidth / 2,
                        classes.user.displayHeight / 2 + 10, (255, 255, 255))

    elif int(High) > int(score):
        physics.message("The High Score is : " + str(High) + "You got : " + str(score), classes.user.displayWidth / 2,
                        classes.user.displayHeight / 2 + 10, (255, 255, 255))
    pygame.display.update()

    while not end:
        print("hi")
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_y:
                    end = True
                    root = Tk()
                    root.geometry("300x200")
                    app = gui.Window(root)
                    app.mainloop()
                    print("tweet")

                if event.key == pygame.K_n:
                    end = True
                    print("Endyyn")


# This is the main menu of my game which will be run as a function
def menufunction():
    # This is a list of all menu images to be looped through
    menus = [users.images + "START.png", users.images + "settings.png", users.images + "highscore.png",
             users.images + "exit.png"]
    menuScreen = True
    x = 0
    menu = pygame.image.load(menus[x])
    # An iterative loop that checks the current menu selection
    while menuScreen:
        if x == -1:
            x = 3
        if x == 4:
            x = 0

        # Updates the screens displays
        pygame.display.update()

        # All user inputs possible
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuScreen = False

            if event.type == pygame.KEYDOWN:

                # Allows arrows and "W/S" to loop through menu
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    x -= 1

                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    x += 1
                    if x == len(menus):
                        x = 0

                # When a user clicks space the current menu item will be initiated
                if event.key == pygame.K_SPACE:
                    if x == 0:
                        maingame()  # Initiates game loop
                    if x == 1:
                        print("Settings")
                    if x == 2:
                        print("Highscore")
                    if x == 3:
                        menuScreen = False

                menu = pygame.image.load(menus[x])
        users.screen.blit(menu, (0, 0))
        pygame.display.update()
