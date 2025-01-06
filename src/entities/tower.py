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
        self.cooldown = self.stats['cooldown'] * 1000
        self.last_shot = 0
        
        # Tower stats tracking
        self.enemies_defeated = 0
        self.shots_fired = 0
        self.damage_dealt = 0
        
        # Selection state
        self.selected = False
    
    def can_shoot(self):
        now = pygame.time.get_ticks()
        can_shoot = now - self.last_shot >= self.cooldown
        if can_shoot:
            print(f"{self.type} tower at {self.rect.center} can shoot")
        return can_shoot
    
    def get_target(self, enemies):
        closest_enemy = None
        closest_dist = self.range  # Use range as the maximum distance
        
        print(f"\nChecking targets for {self.type} tower at {self.rect.center}")
        print(f"Number of enemies: {len(enemies)}")
        
        for enemy in enemies:
            dist = math.hypot(
                enemy.rect.centerx - self.rect.centerx,
                enemy.rect.centery - self.rect.centery
            )
            print(f"Enemy at {enemy.rect.center}, distance: {dist}, range: {self.range}")
            if dist < closest_dist:
                closest_dist = dist
                closest_enemy = enemy
        
        if closest_enemy:
            print(f"Found target at distance {closest_dist}")
        else:
            print("No target found in range")
            
        self.current_target = closest_enemy
        return closest_enemy
    
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
    
    def update(self, enemies=None, projectiles=None):
        print(f"\n{self.type} tower update:")
        if enemies is None or projectiles is None:
            print("No enemies or projectiles provided to tower update")
            return
        
        print(f"Enemies provided: {len(enemies)}")
        print(f"Can shoot: {self.can_shoot()}")
        
        if self.can_shoot():
            target = self.get_target(enemies)
            print(f"Got target: {target is not None}")
            if target:
                print("Attempting to shoot...")
                self.shoot(target, projectiles)
                print(f"Projectiles after shoot: {len(projectiles)}") 