import pygame
import math
from ..core.settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos, damage, speed=8, color=WHITE):
        super().__init__()
        self.pos = pygame.math.Vector2(start_pos)
        self.target = pygame.math.Vector2(target_pos)
        
        # Create tech-themed projectile
        size = 8
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Draw main particle
        pygame.draw.circle(self.image, WHITE, (size//2, size//2), size//2)
        
        # Add glow effect
        glow_size = size * 2
        glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (255, 255, 255, 128), 
                          (glow_size//2, glow_size//2), glow_size//2)
        
        self.image = glow_surf
        self.rect = self.image.get_rect(center=start_pos)
        self.damage = damage
        self.speed = speed
        
        # Trail effect
        self.trail_points = []
        self.max_trail_length = 5
        
        # Calculate direction
        to_target = self.target - self.pos
        self.direction = to_target.normalize() if to_target.length() > 0 else pygame.math.Vector2(0, 0)
        self.initial_pos = start_pos
    
    def update(self):
        # Update trail
        self.trail_points.append(self.pos.copy())
        if len(self.trail_points) > self.max_trail_length:
            self.trail_points.pop(0)
        
        # Move towards target
        self.pos += self.direction * self.speed
        self.rect.center = self.pos
        
        if (self.pos - self.target).length() < self.speed:
            self.kill()
    
    def draw(self, surface):
        # Draw trail
        if len(self.trail_points) > 1:
            points = [(int(p.x), int(p.y)) for p in self.trail_points]
            pygame.draw.lines(surface, (255, 255, 255, 128), False, points, 2)
        
        # Draw projectile
        surface.blit(self.image, self.rect) 