import pygame
import math
import random as r


BG_COLOR = (150, 150, 200)
BUBBLE_COLOR = (50, 50, 255)
BUBBLE_RADIUS = 90
BUBBLE_WIDTH = 2
CHILD_NUMBERS = [6, 10, 10, 10, 15, 15, 15, 30]

INITIAL_SPEED = 5
OUTWARD_DECELERATION = .05
INWARD_ACCELERATION = .05


class Bubble():
    
    def __init__(self):
        self.color = BUBBLE_COLOR
        self.radius = BUBBLE_RADIUS
        self.width = BUBBLE_WIDTH
        
        self.x, self.y = pygame.mouse.get_pos()
        
        self.popped = False
    
    def move(self):
        self.x, self.y = pygame.mouse.get_pos()
    
    def draw(self, surface):
        if self.radius > 0:
            pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius, self.width) 
    
    def pop(self):
        if self.popped:
            return
        else:
            self.popped = True
            children = []
            number_of_children = r.choice(CHILD_NUMBERS)
            for i in range(number_of_children):
                child_radius = self.radius // number_of_children
                child_direction = 360 // number_of_children * i
                child = ChildBubble(self.x, self.y, child_radius, child_direction)
                children.append(child)
            self.radius = 0
            return children


class ChildBubble():
    
    def __init__(self, x, y, radius, direction):
        self.color = BUBBLE_COLOR
        self.radius = radius
        self.width = BUBBLE_WIDTH
        self.x = x
        self.y = y
        
        self.speed = INITIAL_SPEED
        self.direction = direction
        
        self.moving_outward = True
        self.home = False
    
    def move(self, bubble):
        if self.moving_outward:
            self.x += math.cos(self.direction * (math.pi / 180)) * self.speed
            self.y += math.sin(self.direction * (math.pi / 180)) * self.speed
        
            self.speed -= OUTWARD_DECELERATION
            if self.speed <= 0:
                self.moving_outward = False
        
        elif not self.moving_outward:
            target_x, target_y = pygame.mouse.get_pos()
            self.direction = math.atan2(target_y - self.y, target_x - self.x) * (180 / math.pi)
            self.speed += INWARD_ACCELERATION
            
            self.x += math.cos(self.direction * (math.pi / 180)) * self.speed
            self.y += math.sin(self.direction * (math.pi / 180)) * self.speed
            
            distance_from_home = ((self.x - target_x) ** 2 + (self.y - target_y) ** 2) ** 0.5
            if distance_from_home <= bubble.radius + self.radius:
                self.home = True
                bubble.radius += self.radius
                self.radius = 0
            
            
    
    def draw(self, surface):
        if not self.home:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius, self.width)
        
        
        


def run_game():
    # Initialize game and create screen object.
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption('Bubbles 1')
    
    #pygame.mouse.set_visible(False)
    
    bubble = Bubble()
    children = []
    
    running = True
    
    # Start the main loop for the game.
    while running:
        
        screen.fill(BG_COLOR)
        
        bubble.move()
        bubble.draw(screen)
        
        for child in children:
            child.move(bubble)
            child.draw(screen)
        
        # get rid of children that got home (radius 0)
        children = [child for child in children if child.radius > 0]
        if children == []:
            bubble.popped = False
        
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not bubble.popped:
                children = bubble.pop()
            if event.type == pygame.QUIT:
               running = False
        
        # Make the most recently drawn screen visible
        pygame.display.flip()

run_game()
