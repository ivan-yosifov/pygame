import pygame
import random

pygame.init()

sw = 800
sh = 800

ogY = 650
speed  = 3

bg = pygame.image.load('gameAssets/spaceWithMoon.png')
ast = pygame.image.load('gameAssets/asteroid28.png')
doge = pygame.image.load('gameAssets/dogeRocket.png')

music = pygame.mixer.music.load('gameAssets/dogeCoinSong.mp3')
pygame.mixer.music.play(-1)

clock= pygame.time.Clock()

win = pygame.display.set_mode((sw, sh))

class Thing():
    def isCollision(self, thing):
        if self.x < thing.x + thing.w and self.x + self.w > thing.x + thing.w:
            if self.y < thing.y + thing.h and self.y + self.h > thing.y:
                return True

        if self.x + self.w > thing.x and self.x < thing.x:
            if self.y < thing.y + thing.h and self.y + self.h > thing.y:
                return True
        return False

class Player(Thing):
    def __init__(self, x):
        self.x = x
        self.y = ogY
        self.w = 50
        self.h = 100
        self.yv = 0
        self.image = doge
        self.score = 0

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def update_speed(self):
        self.y += self.yv

    def checkIncreaseScore(self):
        if self.y <= 100:
            self.score += 1
            self.y = ogY

class Rock(Thing):
    def __init__(self):
        self.w = 28
        self.h = 28
        self.image = ast
        self.y = random.randint(108, sh - 200 - self.h)
        randX = random.choice([0, 1])
        if randX == 0:
            self.x = -50 - self.w
            self.xv = 2
        else:
            self.x = sw + 50
            self.xv = -2

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.xv



def redrawGameWindow():
    win.blit(bg, (0, 0))
    p1.draw(win)
    p2.draw(win)
    for rock in rocks:
        rock.draw(win)

    font = pygame.font.SysFont('arial', 50)
    p1ScoreText = font.render(str(p1.score), 1, (255,255,255))
    p2ScoreText = font.render(str(p2.score), 1, (255,255,255))
    win.blit(p1ScoreText, (200 - p1ScoreText.get_width()/2, 740))
    win.blit(p2ScoreText, (600 - p2ScoreText.get_width()/2, 740))

    pygame.display.update()

p1 = Player(175)
p2 = Player(575)

rocks = []
count = 0

run = True
while run:
    clock.tick(100)

    p1.update_speed()
    p2.update_speed()

    p1.checkIncreaseScore()
    p2.checkIncreaseScore()

    count += 1
    if count % 60 == 0:
        rocks.append(Rock())
        rocks.append(Rock())

    for rock in rocks:
        rock.move()

        if rock.xv > 0 and rock.x > sw:
            rocks.pop(rocks.index(rock))
        if rock.xv < 0 and rock.x < -rock.w:
            rocks.pop(rocks.index(rock))

        if p1.isCollision(rock):
            rocks.pop(rocks.index(rock))
            p1.y = ogY

        if p2.isCollision(rock):
            rocks.pop(rocks.index(rock))
            p2.y = ogY

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                p2.yv = speed
            if event.key == pygame.K_UP:
                p2.yv = -speed
            if event.key == pygame.K_s:
                p1.yv = speed
            if event.key == pygame.K_w:
                p1.yv = -speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                p2.yv = 0
            if event.key == pygame.K_UP:
                p2.yv = 0
            if event.key == pygame.K_s:
                p1.yv = 0
            if event.key == pygame.K_w:
                p1.yv = 0

    redrawGameWindow()

pygame.quit()
