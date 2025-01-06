import pygame
from ..core.settings import *

class WaveManager:
    def __init__(self, game):
        self.game = game
        self.current_wave = 0
        self.wave_in_progress = False
        self.enemies_to_spawn = []
        self.last_spawn_time = 0
        self.spawn_delay = 1000
        self.wave_completed = True
    
    def start_wave(self):
        if self.wave_completed and self.current_wave < len(WAVE_CONFIGS):
            self.wave_in_progress = True
            self.wave_completed = False
            wave_config = WAVE_CONFIGS[self.current_wave]
            
            # Create list of enemies to spawn
            self.enemies_to_spawn = []
            for enemy_type, count in wave_config['enemies']:
                self.enemies_to_spawn.extend([enemy_type] * count)
            
            self.spawn_delay = wave_config['spawn_delay'] * 1000  # Convert to milliseconds
            self.current_wave += 1
            return True
        return False
    
    def update(self):
        current_time = pygame.time.get_ticks()
        
        # Spawn enemies
        if self.wave_in_progress and self.enemies_to_spawn:
            if current_time - self.last_spawn_time > self.spawn_delay:
                enemy_type = self.enemies_to_spawn.pop(0)
                self.game.spawn_enemy(enemy_type)
                self.last_spawn_time = current_time
        
        # Check if wave is complete
        if self.wave_in_progress and not self.enemies_to_spawn and not self.game.enemies:
            self.wave_in_progress = False
            self.wave_completed = True
            self.game.wave_completed() 