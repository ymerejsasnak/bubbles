import pygame
import math
import random as r


BG_COLOR = (150, 150, 200)
BUBBLE_COLOR = (100, 100, 250)
BUBBLE_RADIUS = 90
BUBBLE_WIDTH = 1
MIN_CHILDREN = 20
MAX_CHILDREN = 50

INITIAL_SPEED = 5
OUTWARD_DECELERATION = .05
INWARD_ACCELERATION = .05


def area(r):
    return math.pi * r ** 2
    

class Bubble():
    
    def __init__(self):
        self.color = BUBBLE_COLOR
        self.radius = BUBBLE_RADIUS
        self.width = BUBBLE_WIDTH
        
        self.x, self.y = pygame.mouse.get_pos()
        
        self.popped = False
        self.popped_twice = False
    
    def move(self):
        self.x, self.y = pygame.mouse.get_pos()
    
    def draw(self, surface):
        if self.radius > 0:
            pygame.draw.circle(surface, self.color, (self.x, self.y), int(self.radius), self.width) 
    
    def pop_it(self, children):
        if self.popped and self.popped_twice:
            return
        elif not self.popped:
            self.popped = True
            children = []
            number_of_children = r.randint(MIN_CHILDREN, MAX_CHILDREN + 1)
            
            child_radius = ((area(self.radius) / number_of_children) / math.pi) ** (1/2)
            
            for i in range(number_of_children):
                child_direction = 360 / number_of_children * i
                child = ChildBubble(self.x, self.y, child_radius, child_direction)
                children.append(child)
            self.radius = 0
            return children
            
        elif self.popped and not self.popped_twice:
            self.popped_twice = True
            sub_children = []
            number_of_children = r.randint(MIN_CHILDREN, MAX_CHILDREN + 1)
            
            sub_child_radius = ((area(children[0].radius) / number_of_children) / math.pi) ** (1/2)
            
            for child in children:
                for i in range(number_of_children):
                    sub_child_direction = 360 / number_of_children * i
                    sub_child = ChildBubble(child.x, child.y, sub_child_radius, sub_child_direction)
                    sub_children.append(sub_child)
            return sub_children


class ChildBubble():
    
    def __init__(self, x, y, radius, direction):
        self.color = BUBBLE_COLOR
        self.radius = radius
        self.width = BUBBLE_WIDTH
        self.x = x
        self.y = y
        
        self.speed = r.uniform(INITIAL_SPEED - 1, INITIAL_SPEED + 1) 
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
                new_area = area(bubble.radius) + area(self.radius)
                bubble.radius  = (new_area / math.pi) ** 0.5
                self.radius = 0
            
            
    
    def draw(self, surface):
        if not self.home:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius), self.width)
        
        
        


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
            bubble.popped_twice = False
        
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not bubble.popped_twice:
                children = bubble.pop_it(children)
            if event.type == pygame.QUIT:
               running = False
        
        # Make the most recently drawn screen visible
        pygame.display.flip()

run_game()
