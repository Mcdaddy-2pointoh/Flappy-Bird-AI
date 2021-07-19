import pygame as pg
import random


# SCREEN DIMENSIONS
WIDTH = 483
HEIGHT = 700

# IMAGES
BIRD_IMAGE = [pg.transform.scale2x(pg.image.load("./Images/bird1.png")),
              pg.transform.scale2x(pg.image.load("./Images/bird3.png")),
              pg.transform.scale2x(pg.image.load("./Images/bird2.png"))]
PIPE_IMAGE = pg.transform.scale2x(pg.image.load("./Images/pipe.png"))
BASE_IMAGE = pg.transform.scale2x(pg.image.load("./Images/base.png"))
BG = pg.transform.scale2x(pg.image.load("./Images/bg.png"))
pg.font.init()

# SCORE
STAT_FONT = pg.font.SysFont("comicsans", 50)


# BIRD OBJECT
class Bird:
    IMAGES = BIRD_IMAGE
    MAX_ROTATION = 25
    ROT_VEL = 60
    ANIMATION_TIME = 100

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.image_count = 0
        self.image = self.IMAGES[self.image_count]

    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        d = (self.velocity*self.tick_count) + 1.5*(self.tick_count**2)

        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION

            else:
                if self.tilt > -90:
                    self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.image_count += 1

        if self.image_count < self.ANIMATION_TIME:
            self.image = self.IMAGES[0]

        elif self.image_count < self.ANIMATION_TIME*2:
            self.image = self.IMAGES[1]

        elif self.image_count < self.ANIMATION_TIME*3:
            self.image = self.IMAGES[2]

        elif self.image_count < self.ANIMATION_TIME*4:
            self.image = self.IMAGES[1]

        elif self.image_count == self.ANIMATION_TIME * 4 + 1:
            self.image = self.IMAGES[0]
            self.image_count = 0

        if self.tilt <= -80:
            self.image = self.IMAGES[1]
            self.image_count = self.ANIMATION_TIME*2

        rotated_image = pg.transform.rotate(self.image, self.tilt)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pg.mask.from_surface(self.image)


# PIPE OBJECT
class Pipe:
    GAP = random.randint(0, 220)
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.pipe_top = pg.transform.flip(PIPE_IMAGE, False, True)
        self.pipe_bottom = PIPE_IMAGE
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randint(50, 450)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.top + self.GAP + random.randint(675, 680)

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.pipe_top, (self.x, self.top))
        win.blit(self.pipe_bottom, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pg.mask.from_surface(self.pipe_top)
        bottom_mask = pg.mask.from_surface(self.pipe_bottom)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True


# BASE CLASS
class Base:
    VEL = 5
    WIDTH = BASE_IMAGE.get_width()
    IMAGE = BASE_IMAGE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMAGE, (self.x1, self.y))
        win.blit(self.IMAGE, (self.x2, self.y))


# WINDOW FUNCTION
def draw_window(win, bird, pipes, base, score):
    win.blit(BG, (0, 0))
    bird.draw(win)
    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    text = STAT_FONT.render("Score:" + str(score), True, (255, 255, 255))
    win.blit(text, (WIDTH - 10 - text.get_width(), 10))
    pg.display.update()


# MAIN GAME LOOP
def main():
    bird = Bird(200, 200)
    pipes = [Pipe(500)]
    base = Base(600)
    win = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    run = True
    score = 0
    while run:
        add_pipe = False
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        rem = []
        # bird.move()
        for pipe in pipes:
            if pipe.collide(bird):
                pass

            if pipe.x + pipe.pipe_top.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            pipe.move()

        base.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(500))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.image.get_height() > 600:
            pass

        draw_window(win, bird, pipes, base, score)
    pg.quit()
    quit()


main()
