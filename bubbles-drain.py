import pygame
import math
import random as r

SCR_WIDTH = 1200
SCR_HEIGHT = 800
SCR_CENTER = (SCR_WIDTH // 2, SCR_HEIGHT // 2)
TARGET_X = SCR_CENTER[0]
TARGET_Y = SCR_CENTER[1]

X_ORIGINS = [x for x in range(SCR_WIDTH) if x < SCR_WIDTH / 3 or x > SCR_WIDTH / 3 * 2]
Y_ORIGINS = [y for y in range(SCR_HEIGHT) if y < SCR_HEIGHT / 3 or y > SCR_HEIGHT / 3 * 2]

BG_COLOR = (150, 150, 200)
BUBBLE_COLOR = (50, 50, 250)
BUBBLE_WIDTH = 1

MEDIAN_RADIUS = 20
RADIUS_VARIATION = 2
RADIUS_CHANGE = .99

MAX_BUBBLES = 1000

MEDIAN_INITIAL_SPEED = .1
SPEED_VARIATION = .05
MAX_SPEED = 1.5

MEDIAN_ACCELERATION = .05
ACCELERATION_VARIATION = .01

MEDIAN_ROTATION = 50
ROTATION_VARIATION = 10




class Bubble():
    
    def __init__(self):
        self.color = BUBBLE_COLOR
        self.radius = r.randint(MEDIAN_RADIUS - RADIUS_VARIATION, MEDIAN_RADIUS + RADIUS_VARIATION) 
        self.width = BUBBLE_WIDTH
        
        self.x = r.choice(X_ORIGINS)
        self.y = r.choice(Y_ORIGINS)
        
        self.speed = r.uniform(MEDIAN_INITIAL_SPEED - SPEED_VARIATION, MEDIAN_INITIAL_SPEED + SPEED_VARIATION)
        self.acceleration = r.uniform(MEDIAN_ACCELERATION - ACCELERATION_VARIATION, MEDIAN_ACCELERATION + ACCELERATION_VARIATION)
        self.rotation = r.randint(MEDIAN_ROTATION - ROTATION_VARIATION, MEDIAN_ROTATION + ROTATION_VARIATION)
        
        self.direction = math.atan2(TARGET_Y- self.y, TARGET_X - self.x) * (180 / math.pi)

        self.home = False
    
    def move(self):
        self.speed = max(self.speed + self.acceleration, MAX_SPEED)
        
        self.radius = max(self.radius * RADIUS_CHANGE, 1)

        self.direction = math.atan2(TARGET_Y - self.y, TARGET_X - self.x) * (180 / math.pi)     
        self.direction += self.rotation   
        
        self.x += math.cos(self.direction * (math.pi / 180)) * self.speed
        self.y += math.sin(self.direction * (math.pi / 180)) * self.speed
            
        distance_from_home = ((self.x - TARGET_X) ** 2 + (self.y - TARGET_Y) ** 2) ** 0.5
        if distance_from_home <= MEDIAN_RADIUS * 2:
            self.home = True
    
    def draw(self, surface):
        if not self.home:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius), self.width) 


def run_game():
    # Initialize game and create screen object.
    pygame.init()
    screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
    pygame.display.set_caption('Bubbles 1')
    
    #pygame.mouse.set_visible(False)
    
    bubbles = []
    running = True
    
    # Start the main loop for the game.
    while running:
        
        screen.fill(BG_COLOR)
        
        if len(bubbles) < MAX_BUBBLES:
            bubbles.append(Bubble())
            bubbles.append(Bubble())
        
        for bubble in bubbles:
            bubble.move()
            bubble.draw(screen)
        
        # get rid of bubbles that got home
        bubbles = [bubble for bubble in bubbles if not bubble.home]
        
        
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False
        
        # Make the most recently drawn screen visible
        pygame.display.flip()

run_game()
