#################################################################
# Name: Ujjen Rajkarnikar
# Date: 19-01-2022
# Description: A Corona Virus Simulation
#################################################################

import pygame
import random

# Defining colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

WIDTH = 800
HEIGHT = 600
BALL_SIZE = 5

# Person class
class Person:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.healthy = "WHITE"

    # the distance function
    def dist(self, peep):
        x1 = self.x
        y1 = self.y
        x2 = peep.x
        y2 = peep.y
        distance = (((x1-x2)**2) + ((y1-y2)**2))**(1/2)
        return float(distance)

    # the collision function
    def collision(self, other):
        if self.dist(other) <= 10.0:
            self.dx *= -1
            self.dy *= -1
            other.dx *= -1
            other.dx *= -1

            #checking for infection
            if(self.healthy == "RED"):
                other.healthy = "RED"

            elif(other.healthy == "RED"):
                self.healthy = "RED"



# making a new random ball
def make_ball():
    person = Person()

    #starting position of a ball
    person.x = random.randrange(BALL_SIZE, WIDTH - BALL_SIZE)
    person.y = random.randrange(BALL_SIZE, HEIGHT - BALL_SIZE)

    #speed and diretion of rectangle
    person.dx = random.randrange(-2,3)
    person.dy = random.randrange(-2,3)

    # WHITE indicates healthy and RED indicates infected
    person.healthy = "WHITE"

    return person


# main game program
def main():
    # Initializing pygame
    pygame.init()

    # create the screen
    screen = pygame.display.set_mode((WIDTH,HEIGHT))

    # Title and Icon
    pygame.display.set_caption("Corona virus simulation")
    icon = pygame.image.load('virus.png')
    pygame.display.set_icon(icon)

    # Loop until the user clicks the close button
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    person_list = []

    for i in range(51):
        person = make_ball()
        person_list.append(person)



    # MAIN PROGRAM LOOP
    while not done:
        # Event processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for i in range(11):
                        person = make_ball()
                        person_list.append(person)

        # Logic
        for person in person_list:
            # Moves the ball's center
            person.x += person.dx
            person.y += person.dy

            # Bounce the ball
            if person.y > HEIGHT - BALL_SIZE or person.y < BALL_SIZE:
                person.dy *= -1
            if person.x > WIDTH - BALL_SIZE or person.x < BALL_SIZE:
                person.dx *= -1


        # set the screen background
        screen.fill(BLACK)

        # The first person is infected
        person_list[0].healthy = "RED"

        # collision
        for person in person_list:

            # for all the other balls:
            for i in range(0,len(person_list)):
                if person != person_list[i]:
                    person.collision(person_list[i])

                    # drawing the balls
                    pygame.draw.circle(screen, person.healthy, [person.x, person.y], BALL_SIZE)

        # Limit to 60 frames per second
        clock.tick(60)

        pygame.display.flip()

    # Close everything down
    pygame.quit()

if __name__ == "__main__":
    main()
