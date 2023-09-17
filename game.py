import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
GREEN1 = (0, 255, 0)
GREEN2 = (0, 150, 0)
BLACK = (0,0,0)
GOLD = (255, 223, 0)
GREEN3 = (0, 128, 0)
GREEN4 = (34, 139, 34)
PURPLE1 = (128, 0, 128)    # Standard Purple
PURPLE2 = (102, 0, 102)
SQUARE_SIZE = 50
BLOCK_SIZE = 20
SPEED = 20

class SnakeGame:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()
    
    def reset(self):
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iter = 0
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self, action):
        self.frame_iter += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iter > 100 * len(self.snake):
            game_over = True
            reward = -100
            return reward, game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 100
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score
    
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False
        
    def _update_ui(self):
       #self.display.fill(GREEN1)
       #pygame.draw.rect(self.display, GREEN1, pygame.Rect(BORDER_SIZE, BORDER_SIZE, self.w - 2 * BORDER_SIZE, self.h - 2 * BORDER_SIZE))
        for y in range(0, 480, SQUARE_SIZE):
            # For each column
            for x in range(0, 640, SQUARE_SIZE):
                if (x // SQUARE_SIZE) % 2 == (y // SQUARE_SIZE) % 2:
                    color = GREEN1
                else:
                    color = GREEN2
                
                pygame.draw.rect(self.display, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
        for pt in self.snake:
            pygame.draw.rect(self.display, PURPLE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, PURPLE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        # Draw the apple
        pygame.draw.circle(self.display, RED, (self.food.x + BLOCK_SIZE // 2, self.food.y + BLOCK_SIZE // 2), BLOCK_SIZE // 2)

        # Draw the leaf on the apple
        pygame.draw.arc(self.display, GREEN3, (self.food.x + BLOCK_SIZE // 4, self.food.y, BLOCK_SIZE // 2, BLOCK_SIZE // 2), 5 * np.pi / 6, 7 * np.pi / 6, 2)

        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, action):
        right = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        index = right.index(self.direction)

        if np.array_equal(action, [1,0,0]):
            new_dir = right[index]
        elif np.array_equal(action, [0,1,0]):
            next = (index + 1) % 4
            new_dir = right[next]
        else:
            next = (index - 1) % 4
            new_dir = right[next]
        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
