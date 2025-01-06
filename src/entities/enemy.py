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
        self.reached_end = False
        
        # Convert grid coordinates to pixel coordinates for starting position
        start_x = path_points[0][0] * TILE_SIZE + TILE_SIZE // 2
        start_y = path_points[0][1] * TILE_SIZE + TILE_SIZE // 2
        self.rect.center = (start_x, start_y)
        
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
    
    def update(self, time_delta):
        if self.path_index >= len(self.path_points) - 1:
            self.reached_end = True
            return
            
        # Get current and next points
        current = self.path_points[self.path_index]
        next_point = self.path_points[self.path_index + 1]
        
        # Convert grid coordinates to pixels
        next_pos = (next_point[0] * TILE_SIZE + TILE_SIZE // 2,
                   next_point[1] * TILE_SIZE + TILE_SIZE // 2)
        
        # Calculate direction and distance
        dx = next_pos[0] - self.rect.centerx
        dy = next_pos[1] - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Move towards next point with speed scaled by time_delta
        speed = self.stats['speed'] * time_delta * 60  # Scale to maintain same base speed
        
        # If we're very close to the target point or can reach it this frame
        if distance <= speed or distance < 1:
            # Snap to the waypoint
            self.rect.centerx = next_pos[0]
            self.rect.centery = next_pos[1]
            self.path_index += 1
        else:
            # Move proportionally
            move_x = (dx / distance) * speed
            move_y = (dy / distance) * speed
            self.rect.x += move_x
            self.rect.y += move_y
    
    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0 