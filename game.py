import tkinter as tk
from tkinter import messagebox
import pygame
import random
import  math
pygame.init()


class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        print(self.pos[0])
        p1 = self.pos[0]
        p2 = self.pos[1]
        pygame.draw.rect(surface, self.color, (p1 * dis + 1, p2 * dis + 1, dis - 2, dis - 2))
        if eyes:
            center = dis // 2
            radius = 3
            circleMiddle = (p1 * dis + center - radius, p2 * dis + 8)

            circleMiddle2 = (p1 * dis + dis - 2 * radius, p2 * dis + 8)  # two centers for 2 eyes

            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake(object):
    body = []    # snake body will be a list of cubes
    turns = {}   # turns will be a dictionar with key value pairs which will store
                 # where the snake has to move

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()  # keys will contain a list of all the key values that were pressed
            for ki in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
                currcubePos = c.pos[:]
                if currcubePos in self.turns:
                    print('yo')
                    turn = self.turns[currcubePos]  # turn stores the direction in which we have to turn
                    c.move(turn[0], turn[1])
                    if i == len(self.body) - 1:
                        self.turns.pop(currcubePos)
                else:
                    if c.dirnx == -1 and c.pos[0] <= 0:
                        c.pos = (c.rows - 1, c.pos[1])
                    elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                        c.pos = (0, c.pos[1])
                    elif c.dirny == -1 and c.pos[1] <= 0:
                        c.pos = (c.pos[0], c.rows - 1)
                    elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                        c.pos = (c.pos[0], 0)
                    else:
                        c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)  # true parameter for eyes
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    gap_btw_rows = w // rows

    x = 0
    y = 0
    for i in range(rows):
        x = x + gap_btw_rows
        y = y + gap_btw_rows
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface):
    global width, rows, s, snack
    surface.fill((0, 0, 0))  # make the screen balck
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)  # draw the snake grid
    pygame.display.update()  # Display.update can just update specific areas of the screen


# The Python's filter() function takes a lambda function together with a
# list as the arguments. It has the following syntax:
# filter(object, iterable)
# The object here should be a lambda function which returns a boolean
# value. The object will be called for every item in the iterable to do the evaluation. The result is either a True or a False for every
# item. Note that the function can only take one iterable as the input.
# A lambda function, along with the list to be evaluated, is passed to the
# filter() function. The filter() function returns a list of those elements that return True
# when evaluated by the lambda funtion. Consider the example given below:

def randomSnack(rows, snakeObject):  # this function will return position
    # of the random snack ""cube""

    positions = snakeObject.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return (x,y)


def message_box(subject, content):
        root = tk.Tk()   # this creates a new Tkinter window
        root.attributes("-topmost",True)
        root.withdraw() # Currently we make the message box window invsible
        messagebox.showinfo(subject,content)
        try:
            root.destroy()
        except:
            pass



def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255, 0, 0), (10, 10))
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            print(snack.pos)
            print(s.body[0].pos)
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                  print('Score : ',len(s.body))
                  message_box('You Lost','Play Again?..')
                  s.reset((10,10))
                  break

        redrawWindow(win)


main()
