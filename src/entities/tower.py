import pygame
import math
from ..core.settings import *
from .projectile import Projectile

class Tower(pygame.sprite.Sprite):
    def __init__(self, tower_type, pos):
        super().__init__()
        self.type = tower_type
        self.stats = TOWER_TYPES[tower_type]
        
        # Create tower sprite
        self.base_image = pygame.Surface((TILE_SIZE - 4, TILE_SIZE - 4))
        self.base_image.fill(self.stats['color'])
        self.image = self.base_image
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        
        # Stats
        self.damage = self.stats['damage']
        self.range = self.stats['range']
        self.cooldown = self.stats['cooldown']
        self.cooldown_remaining = 0  # Initialize cooldown timer
        
        # Tower stats tracking
        self.enemies_defeated = 0
        self.shots_fired = 0
        self.damage_dealt = 0
        
        # Selection state
        self.selected = False
        self.current_target = None
    
    def can_shoot(self):
        now = pygame.time.get_ticks()
        return now - self.last_shot >= self.cooldown
    
    def get_target(self, enemies):
        in_range_enemies = []
        
        # First, find all enemies in range
        for enemy in enemies:
            dist = math.hypot(
                enemy.rect.centerx - self.rect.centerx,
                enemy.rect.centery - self.rect.centery
            )
            if dist < self.range:
                in_range_enemies.append((enemy, enemy.path_index))
        
        if not in_range_enemies:
            return None
        
        # Sort by path index (descending) to target enemies furthest along the path
        in_range_enemies.sort(key=lambda x: x[1], reverse=True)
        
        # Return the enemy furthest along the path
        self.current_target = in_range_enemies[0][0]
        return self.current_target
    
    def shoot(self, target, projectiles):
        self.last_shot = pygame.time.get_ticks()
        projectile = Projectile(
            self.rect.center,
            target.rect.center,
            self.damage,
            speed=8,
            color=WHITE
        )
        projectiles.add(projectile)
        self.shots_fired += 1
    
    def draw_range(self, surface):
        # Only draw range and target line if selected
        if self.selected:
            # Draw range circle
            pygame.draw.circle(
                surface,
                (*self.stats['color'][:3], 50),
                self.rect.center,
                self.range,
                1
            )
            
            # Draw line to current target if exists
            if self.current_target:
                pygame.draw.line(
                    surface,
                    WHITE,
                    self.rect.center,
                    self.current_target.rect.center,
                    1
                )
    
    def get_stats_text(self):
        return [
            f"Type: {self.type.title()}",
            f"Damage: {self.damage}",
            f"Range: {self.range}",
            f"Enemies Defeated: {self.enemies_defeated}",
            f"Shots Fired: {self.shots_fired}",
            f"Damage Dealt: {self.damage_dealt}"
        ]
    
    def update(self, enemies, projectiles, time_delta):
        if self.cooldown_remaining <= 0:
            # Find target
            target = self.get_target(enemies)
            if target:
                # Create projectile
                projectile = Projectile(
                    self.rect.center,
                    target.rect.center,
                    self.stats['damage'],
                    speed=8,
                    color=WHITE
                )
                projectiles.add(projectile)
                self.shots_fired += 1
                self.current_target = target
                self.cooldown_remaining = self.cooldown
        else:
            # Update cooldown with time_delta
            self.cooldown_remaining = max(0, self.cooldown_remaining - time_delta) 