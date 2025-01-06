import pygame
from ..core.settings import *
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, path_points, wave_scaling=None):
        super().__init__()
        self.type = enemy_type
        self.stats = ENEMY_TYPES[enemy_type].copy()  # Make a copy to modify
        
        # Apply wave scaling if provided
        if wave_scaling:
            self.stats['health'] = int(self.stats['health'] * wave_scaling['health_scale'])
            self.stats['speed'] = self.stats['speed'] * wave_scaling['speed_scale']
            self.stats['reward'] = int(self.stats['reward'] * wave_scaling['health_scale'])  # Scale reward with health
        
        # Create circular enemy sprite with tech effect
        size = TILE_SIZE - 4
        self.base_image = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Draw main circle
        pygame.draw.circle(
            self.base_image,
            self.stats['color'],
            (size // 2, size // 2),
            size // 2
        )
        
        # Add tech pattern
        inner_size = size // 2
        pygame.draw.circle(
            self.base_image,
            (*self.stats['color'][:3], 150),  # Lighter version of color
            (size // 2, size // 2),
            inner_size,
            2
        )
        
        # Add binary pattern (small dots in a circle)
        for i in range(8):
            angle = i * (math.pi / 4)
            x = size // 2 + int(math.cos(angle) * (inner_size - 4))
            y = size // 2 + int(math.sin(angle) * (inner_size - 4))
            pygame.draw.circle(
                self.base_image,
                WHITE,
                (x, y),
                1
            )
        
        self.image = self.base_image
        self.rect = self.image.get_rect()
        
        # Path following
        self.path_points = path_points
        self.path_index = 0
        
        # Convert grid coordinates to pixel coordinates
        start_x = path_points[0][0] * TILE_SIZE + TILE_SIZE // 2
        start_y = path_points[0][1] * TILE_SIZE + TILE_SIZE // 2
        self.pos = pygame.math.Vector2(start_x, start_y)
        self.rect.center = self.pos
        
        # Stats
        self.max_health = self.stats['health']
        self.health = self.max_health
        self.speed = self.stats['speed']
        self.reward = self.stats['reward']
    
    def draw_health_bar(self, surface):
        # Health bar dimensions
        bar_width = self.rect.width + 4
        bar_height = 4
        bar_pos = (self.rect.centerx - bar_width // 2, self.rect.top - 8)
        
        # Draw background (black)
        pygame.draw.rect(surface, BLACK, (*bar_pos, bar_width, bar_height))
        
        # Draw health
        health_width = int(bar_width * (self.health / self.max_health))
        if health_width > 0:
            health_color = GREEN if self.health > self.max_health * 0.6 else \
                          YELLOW if self.health > self.max_health * 0.3 else RED
            pygame.draw.rect(surface, health_color, 
                           (bar_pos[0], bar_pos[1], health_width, bar_height))
    
    def move(self):
        if self.path_index < len(self.path_points) - 1:
            # Get current target point in pixels
            target_x = self.path_points[self.path_index + 1][0] * TILE_SIZE + TILE_SIZE // 2
            target_y = self.path_points[self.path_index + 1][1] * TILE_SIZE + TILE_SIZE // 2
            target = pygame.math.Vector2(target_x, target_y)
            
            # Calculate direction to target
            to_target = target - self.pos
            distance = to_target.length()
            
            if distance < self.speed:
                # Reached the current target point
                self.pos = target
                self.path_index += 1
            else:
                # Move towards target
                direction = to_target.normalize()
                self.pos += direction * self.speed
            
            self.rect.center = self.pos
    
    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0
    
    def update(self):
        self.move() 