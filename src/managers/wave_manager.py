import pygame
from ..core.settings import *

class WaveManager:
    def __init__(self, game):
        self.game = game
        self.current_wave = 0
        self.wave_in_progress = False
        self.enemies_to_spawn = []
        self.spawn_delay = 1.0  # Seconds between enemy spawns
        self.spawn_timer = 0.0  # Timer for next spawn
    
    def start_wave(self):
        if not self.wave_in_progress and self.current_wave < len(WAVE_CONFIGS):
            self.wave_in_progress = True
            wave_config = WAVE_CONFIGS[self.current_wave]
            
            # Create list of enemies to spawn
            self.enemies_to_spawn = []
            for enemy_type, count in wave_config['enemies']:
                self.enemies_to_spawn.extend([enemy_type] * count)
            
            self.spawn_timer = wave_config.get('spawn_delay', 1.0)  # Get spawn delay or default to 1.0
            self.current_wave += 1
            return True
        return False
    
    def update(self, time_delta):
        if not self.wave_in_progress:
            return
        
        # Update spawn timer with time_delta
        self.spawn_timer -= time_delta
        
        if self.spawn_timer <= 0 and self.enemies_to_spawn:
            # Spawn next enemy
            enemy_type = self.enemies_to_spawn.pop(0)
            self.game.spawn_enemy(enemy_type)
            
            # Reset timer for next spawn
            self.spawn_timer = self.spawn_delay
        
        # Check if wave is complete
        if not self.enemies_to_spawn and not self.game.enemies:
            self.wave_in_progress = False
            self.game.wave_completed() 