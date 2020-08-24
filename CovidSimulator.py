'''
Name: John Mai
Assignment: Program 2

'''

'''
Personal Notes
-- > Create your Dot class with attributes for initial and target positions, current position
(which is the same as the initial position in the beginning, and gets updated as the dot moves),
state of the dot (i.e. color). Keep track for each dot whether it is stationary or moving,
whether practicing SD6, whether practicing SIP.

---> Add class attributes to keep track of how many dots are in different states.
You will also want to output these as text while the simulation is running
similar to the one in the Washington Post link. 

---> Keep track of the total number of unexposed, infected, sick, immune, dead dots.

--->Collision detection between dots.

--->Collision avoidance between dots with or without SD6 bubble.

--->Get another dot infected when it is within 6 feet of an infected dot. Update their state and color.

--->Stationary dots to denote people who are following SIP or because they are sick, or dead.

'''

import pygame
import random

pygame.init()

DOT_WIDTH = 5
MOVE_WIDTH = 1
size = (700, 500)
initPopulation = 100

# set colors
initial_Color = (0, 190, 255)

# infected - orange
infected = (255, 165, 0)

# immune = green
immune = (0, 255, 0)

# sick - red
sick_Red = (255, 0, 0)

# dead - black
BLACK = (0, 0, 0)

WHITE = (255, 255, 255)
locations = []
targets = []
CURRENT_DAY = 0
ONE_DAY = 100

# ring around person - grey
RING = (192, 192, 192)

SOCIAL_DISTANCE_PERCENTAGE = 75

screen = pygame.display.set_mode(size)


def location_exists(x, y):
    for location in locations:
        spritex = location[0]
        spritey = location[1]
        if ((abs(spritex - x) < (DOT_WIDTH * 4)) and ((abs(spritey - y) < (DOT_WIDTH * 4)))):
            return True
    return False


def get_random_location(max_iterations=1000):
    x = random.randint(0, size[0])
    y = random.randint(0, size[1])
    count = 0
    while (location_exists(x, y)):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        count += 1
        if (count > max_iterations):
            return None
    return (x, y)


def get_target(x, y):
    tx = random.randint(0, size[0])
    ty = random.randint(0, size[1])
    while ((abs(tx - x) < (DOT_WIDTH * 3)) and (abs(ty - y) < (DOT_WIDTH * 3))):
        tx = random.randint(0, size[0])
        ty = random.randint(0, size[1])
    return (tx, ty)

class Dot(pygame.sprite.Sprite):
    def __init__(self, color, x, y, state="healthy", social_distance=True):
        super().__init__()
        self.x = x
        self.y = y
        self.state = state
        self.social_distance = social_distance
        self.target = get_target(x, y)
        if (state == "sick"):
            self.day_sick = 0
        self.draw_circles(color)

    # draw_circles in order to set height and width of circle and create the bubble
    def draw_circles(self, color):
        self.image = pygame.Surface([DOT_WIDTH * 4, DOT_WIDTH * 4])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.home = (self.x, self.y)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.circle = pygame.draw.circle(self.image, color, [DOT_WIDTH * 2, DOT_WIDTH * 2], DOT_WIDTH)

        if (self.social_distance):
            self.secondcircle = pygame.draw.circle(self.image, RING, [DOT_WIDTH * 2, DOT_WIDTH * 2], DOT_WIDTH * 2, 1)

    # testing case for collision
    def reached_target(self):
        tx, ty = self.target
        x, y = self.x, self.y
        if ((abs(tx - x) < (DOT_WIDTH * 2)) and (abs(ty - y) < (DOT_WIDTH * 2))):
            return True
        return False

    # movement
    def step_towards_target(self):
        nx = self.x
        ny = self.y
        if (nx < self.target[0]):
            nx += MOVE_WIDTH

        elif (nx > self.target[0]):
            nx -= MOVE_WIDTH

        if (ny < self.target[1]):
            ny += MOVE_WIDTH

        elif (ny > self.target[1]):
            ny -= MOVE_WIDTH

        return nx, ny

    # chances of circle getting infected
    def infect_chance(self):
        chances = random.randint(0, 100)
        if (chances < 80):
            self.state = "infected"
            self.day_infected = CURRENT_DAY
            self.draw_circles(infected)

    # sick
    def try_sick(self):
        chances = random.randint(0, 100)
        if (chances < 50):
            self.state = "sick"
            self.day_sick = CURRENT_DAY
            self.draw_circles(sick_Red)

    # immune
    def immunity(self):
        self.state = "immune"
        self.draw_circles(immune)

    # death
    def death(self):
        chances = random.randint(0, 100)
        if (chances < 50):
            self.state = "dead"
            self.draw_circles((0, 25, 51))
        else:
            self.immunity()

    def update(self):
        if (self.state == "infected"):
            if ((CURRENT_DAY - self.day_infected) > 5):
                self.try_sick()
            elif ((CURRENT_DAY - self.day_infected) > 15):
                self.immunity()

        elif (self.state == "sick"):
            if ((CURRENT_DAY - self.day_sick) > 10):
                self.death()
            return

        elif (self.state == "dead"):
            return

        if (self.reached_target()):
            copy = self.target
            self.target = self.home
            self.home = copy
            return

        self.x, self.y = self.step_towards_target()
        self.rect.x = self.x
        self.rect.y = self.y


# COLLISION CODE -> WORK ON  -> IMPORTANT
def process_collisions(population):
    now_infected = []
    for sprite in population:
        if (sprite.state in ["infected", "sick"]):
            infected_list = pygame.sprite.spritecollide(sprite, population, False)
            now_infected.extend(infected_list)

    now_infected = set(now_infected)

    for infected in now_infected:
        if (infected.state == "healthy"):
            if (infected.social_distance):
                willinfect = random.randint(0, 100)
                if (willinfect < 40):
                    infected.infect_chance()
            else:
                infected.infect_chance()


def populate(initPopulation):
    person_sick = random.randint(0, initPopulation - 1)
    population = pygame.sprite.Group()
    global locations

    for i in range(initPopulation):
        pop = get_random_location()
        if (pop == None):
            print("no more space left")
            return population

        distance = random.randint(0, 100)
        Social_Dist = False

        if (distance < SOCIAL_DISTANCE_PERCENTAGE):
            Social_Dist = True
        if (i == person_sick):
            population.add(Dot(sick_Red, pop[0], pop[1], state="sick", social_distance=False))
        else:
            population.add(Dot(initial_Color, pop[0], pop[1], social_distance=Social_Dist))
        locations.append(pop)
    return population


population = populate(initPopulation)

carryOn = True
clock = pygame.time.Clock()
GAME_FONT = pygame.font.SysFont('Times New Roman', 15)

renders = 0

while carryOn:
    days = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
    screen.fill(WHITE)

    text_surface = GAME_FONT.render("DAY: " + str(CURRENT_DAY), True, (0, 0, 0))
    screen.blit(text_surface, (20, 50))

    pygame.display.update()
    population.draw(screen)
    population.update()
    process_collisions(population)
    pygame.display.flip()
    clock.tick(10000)
    renders += 1
    CURRENT_DAY = renders // ONE_DAY

pygame.quit()