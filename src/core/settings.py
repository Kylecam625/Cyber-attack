# Window Settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
FPS = 60
GAME_TITLE = "CS Tower Defense"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
BROWN = (139, 69, 19)

# Game Settings
STARTING_MONEY = 650
STARTING_LIVES = 100

# Path Settings
TILE_SIZE = 32
GRID_WIDTH = (WINDOW_WIDTH - 250) // TILE_SIZE  # Adjust for UI panel
GRID_HEIGHT = WINDOW_HEIGHT // TILE_SIZE

# Define the path waypoints (in grid coordinates)
PATH_WAYPOINTS = [
    (0, 12),           # Start from left
    (6, 12),          # Reduced x coordinates
    (6, 4),
    (12, 4),          # Reduced x coordinates
    (12, 20),
    (18, 20),         # Reduced x coordinates
    (18, 8),
    (24, 8),          # Reduced x coordinates
    (24, 16),
    (30, 16)          # End before UI panel
]

# Enemy Settings
ENEMY_TYPES = {
    'syntax_error': {
        'health': 100,
        'speed': 2,
        'reward': 10,
        'damage': 1,
        'color': RED
    },
    'logic_error': {
        'health': 200,
        'speed': 1.5,
        'reward': 20,
        'damage': 2,
        'color': BLUE
    },
    'memory_leak': {
        'health': 400,
        'speed': 1,
        'reward': 35,
        'damage': 3,
        'color': PURPLE
    },
    'trojan': {
        'health': 150,
        'speed': 3,
        'reward': 25,
        'damage': 2,
        'color': GREEN
    }
}

# Tower Settings
TOWER_TYPES = {
    'firewall': {
        'cost': 100,
        'damage': 20,
        'range': 150,
        'cooldown': 0.3,
        'color': BLUE,
        'description': 'Basic tower with balanced stats'
    },
    'debugger': {
        'cost': 200,
        'damage': 50,
        'range': 180,
        'cooldown': 0.8,
        'color': GREEN,
        'description': 'High damage, slow attack speed'
    },
    'antivirus': {
        'cost': 350,
        'damage': 30,
        'range': 140,
        'cooldown': 0.2,
        'color': RED,
        'description': 'Fast attack speed, area damage'
    },
    'encryption': {
        'cost': 300,
        'damage': 15,
        'range': 120,
        'cooldown': 0.3,
        'color': PURPLE,
        'description': 'Slows enemies in range'
    }
}

# Wave Generation Settings
WAVE_SCALING = {
    'health_multiplier': 1.2,      # Health increases by 20% each wave
    'count_multiplier': 1.15,      # Enemy count increases by 15% each wave
    'speed_multiplier': 1.05,      # Speed increases by 5% each wave
    'reward_multiplier': 1.1,      # Rewards increase by 10% each wave
    'base_counts': {
        'syntax_error': 10,
        'logic_error': 5,
        'memory_leak': 2,
        'trojan': 3
    }
}

def generate_waves(num_waves=100):
    waves = []
    
    for wave_num in range(num_waves):
        # Calculate scaling factors based on wave number
        health_scale = WAVE_SCALING['health_multiplier'] ** (wave_num // 5)
        count_scale = WAVE_SCALING['count_multiplier'] ** (wave_num // 3)
        speed_scale = WAVE_SCALING['speed_multiplier'] ** (wave_num // 8)
        
        # Determine which enemies appear in this wave
        enemies = []
        
        # Syntax errors appear in all waves
        if wave_num >= 0:
            count = int(WAVE_SCALING['base_counts']['syntax_error'] * count_scale)
            enemies.append(('syntax_error', count))
        
        # Logic errors appear after wave 5
        if wave_num >= 5:
            count = int(WAVE_SCALING['base_counts']['logic_error'] * (count_scale * 0.8))
            enemies.append(('logic_error', count))
        
        # Trojans appear after wave 10
        if wave_num >= 10:
            count = int(WAVE_SCALING['base_counts']['trojan'] * (count_scale * 0.6))
            enemies.append(('trojan', count))
        
        # Memory leaks appear after wave 15
        if wave_num >= 15:
            count = int(WAVE_SCALING['base_counts']['memory_leak'] * (count_scale * 0.4))
            enemies.append(('memory_leak', count))
        
        # Special waves every 10 waves
        if wave_num > 0 and wave_num % 10 == 0:
            # Boss wave - lots of memory leaks and stronger enemies
            enemies = [
                ('memory_leak', int(10 * count_scale)),
                ('trojan', int(15 * count_scale)),
                ('logic_error', int(20 * count_scale))
            ]
        
        # Calculate spawn delay (gets shorter in later waves)
        spawn_delay = max(0.2, 1.0 - (wave_num * 0.01))
        
        waves.append({
            'enemies': enemies,
            'spawn_delay': spawn_delay,
            'health_scale': health_scale,
            'speed_scale': speed_scale
        })
    
    return waves

# Generate 100 waves
WAVE_CONFIGS = generate_waves(100) 