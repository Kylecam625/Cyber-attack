# Window Settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
FPS = 60
GAME_TITLE = "CS Tower Defense"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 100)
BLUE = (50, 100, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 50)
PURPLE = (180, 50, 255)
BROWN = (139, 69, 19)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
NEON_GREEN = (57, 255, 20)
PINK = (255, 192, 203)

# UI Colors
UI_BACKGROUND = (40, 42, 54)  # Dark theme background
UI_ACCENT = (98, 114, 164)    # Accent color
UI_TEXT = (248, 248, 242)     # Light text
UI_HOVER = (68, 71, 90)       # Hover state
UI_SELECTED = (80, 250, 123)  # Selected state

# Visual Effects
GLOW_EFFECT = True
PARTICLE_EFFECTS = True
TRAIL_LENGTH = 5  # For projectile trails
GLOW_RADIUS = 20
GLOW_INTENSITY = 150  # Alpha value for glow effect

# Tower Visual Settings
TOWER_GLOW_COLORS = {
    'basic_compiler': (50, 150, 255, 100),    # Light blue glow
    'code_injector': (255, 100, 100, 100),    # Light red glow
    'static_analyzer': (100, 255, 100, 100),  # Light green glow
    'recursive_function': (255, 150, 50, 100), # Orange glow
    'async_processor': (150, 50, 255, 100),   # Purple glow
    'exception_handler': (255, 50, 50, 100),  # Red glow
    'cache_freezer': (200, 200, 255, 100),    # Ice blue glow
    'garbage_collector': (100, 255, 200, 100), # Mint green glow
    'quantum_computer': (255, 215, 0, 100),   # Gold glow
    'network_router': (50, 200, 200, 100),    # Teal glow
    'bitcoin_miner': (255, 200, 0, 100),      # Yellow gold glow
    'stack_overflow': (200, 200, 200, 100)    # Silver glow
}

# Enemy Visual Settings
ENEMY_GLOW_COLORS = {
    'syntax_error': (255, 50, 50, 100),    # Red glow
    'logic_error': (50, 100, 255, 100),    # Blue glow
    'memory_leak': (50, 255, 100, 100),    # Green glow
    'trojan': (255, 255, 50, 100)          # Yellow glow
}

# Game Settings
STARTING_MONEY = 650
STARTING_LIVES = 100
NORMAL_GAME_SPEED = 1.0
FAST_FORWARD_SPEED = 2.0  # Double speed for fast forward

# Path Settings
TILE_SIZE = 32
GRID_WIDTH = (WINDOW_WIDTH - 250) // TILE_SIZE  # Adjust for UI panel
GRID_HEIGHT = WINDOW_HEIGHT // TILE_SIZE

# Path Visual Settings
PATH_GLOW = True
PATH_PULSE_SPEED = 0.05  # Speed of path pulsing effect
PATH_PULSE_MIN = 0.4    # Minimum path opacity
PATH_PULSE_MAX = 0.8    # Maximum path opacity

# Grid Visual Settings
GRID_OPACITY = 0.15
GRID_LINE_COLOR = (100, 100, 100)
GRID_HOVER_COLOR = (150, 150, 150, 30)

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
        'health': 1,
        'speed': 2,
        'reward': 1,
        'damage': 1,
        'color': RED
    },
    'logic_error': {
        'health': 2,
        'speed': 1.8,
        'reward': 2,
        'damage': 1,
        'color': BLUE
    },
    'memory_leak': {
        'health': 3,
        'speed': 1.6,
        'reward': 3,
        'damage': 1,
        'color': GREEN
    },
    'trojan': {
        'health': 4,
        'speed': 3.2,
        'reward': 4,
        'damage': 1,
        'color': YELLOW
    }
}

# Tower Settings
TOWER_TYPES = {
    'basic_compiler': {  # Dart Monkey equivalent
        'cost': 200,
        'damage': 1,
        'range': 150,
        'cooldown': 0.95,
        'color': (50, 150, 255),  # Light blue
        'description': 'Basic compiler that catches simple syntax errors. Fast compilation, low processing power.'
    },
    'code_injector': {  # Tack Shooter equivalent
        'cost': 360,
        'damage': 1,
        'range': 100,
        'cooldown': 1.2,
        'color': (255, 100, 100),  # Light red
        'description': 'Injects code in all directions, short range but good coverage.'
    },
    'static_analyzer': {  # Sniper Monkey equivalent
        'cost': 350,
        'damage': 2,
        'range': 1000,  # Unlimited range
        'cooldown': 2.0,
        'color': (100, 255, 100),  # Light green
        'description': 'Long-range code analysis, high damage but slow processing speed.'
    },
    'recursive_function': {  # Boomerang equivalent
        'cost': 380,
        'damage': 3,
        'range': 180,
        'cooldown': 1.5,
        'color': (255, 150, 50),  # Orange
        'description': 'Throws recursive calls that return to source, hitting bugs multiple times.'
    },
    'async_processor': {  # Ninja Monkey equivalent
        'cost': 500,
        'damage': 1,
        'range': 130,
        'cooldown': 0.5,
        'color': (150, 50, 255),  # Purple
        'description': 'Fast async operations that can detect hidden memory leaks.'
    },
    'exception_handler': {  # Bomb Tower equivalent
        'cost': 650,
        'damage': 3,
        'range': 140,
        'cooldown': 1.8,
        'color': (255, 50, 50),  # Red
        'description': 'Throws exceptions that explode on impact, affecting all nearby bugs.'
    },
    'cache_freezer': {  # Ice Tower equivalent
        'cost': 300,
        'damage': 1,
        'range': 100,
        'cooldown': 1.0,
        'color': (200, 200, 255),  # Ice blue
        'description': 'Freezes processes in cache, slowing down bugs temporarily.'
    },
    'garbage_collector': {  # Glue Gunner equivalent
        'cost': 270,
        'damage': 1,
        'range': 120,
        'cooldown': 1.1,
        'color': (100, 255, 200),  # Mint green
        'description': 'Marks bugs for garbage collection, slowing them down.'
    },
    'quantum_computer': {  # Super Monkey equivalent
        'cost': 3500,
        'damage': 1,
        'range': 200,
        'cooldown': 0.1,
        'color': (255, 215, 0),  # Gold
        'description': 'Extremely fast quantum calculations, massive processing power.'
    },
    'network_router': {  # Monkey Village equivalent
        'cost': 1600,
        'damage': 0,
        'range': 150,
        'cooldown': 0,
        'color': (50, 200, 200),  # Teal
        'description': 'Improves nearby towers through network optimization.'
    },
    'bitcoin_miner': {  # Banana Farm equivalent
        'cost': 1000,
        'damage': 0,
        'range': 0,
        'cooldown': 10.0,
        'color': (255, 200, 0),  # Yellow gold
        'description': 'Generates cryptocurrency over time for additional income.'
    },
    'stack_overflow': {  # Spike Factory equivalent
        'cost': 750,
        'damage': 5,
        'range': 100,
        'cooldown': 3.0,
        'color': (200, 200, 200),  # Silver
        'description': 'Creates stack overflow errors that damage bugs passing over them.'
    }
}

# Tower Descriptions with strengths and weaknesses
TOWER_INFO = {
    'basic_compiler': {
        'name': 'Basic Compiler',
        'role': 'Early Game Defense',
        'strengths': '- Fast attack speed\n- Good all-around tower\n- Cheap and efficient',
        'weaknesses': '- Low damage\n- Limited range\n- No special abilities',
        'tips': 'Perfect for early waves. Place multiple for better coverage.'
    },
    'code_injector': {
        'name': 'Code Injector',
        'role': 'Area Control',
        'strengths': '- Hits multiple targets\n- 360-degree coverage\n- Good for clusters',
        'weaknesses': '- Short range\n- Moderate damage\n- Fixed attack pattern',
        'tips': 'Place at intersections or where paths overlap.'
    },
    'static_analyzer': {
        'name': 'Static Analyzer',
        'role': 'Long Range Support',
        'strengths': '- Unlimited range\n- High single-target damage\n- Can hit anywhere',
        'weaknesses': '- Slow attack speed\n- No splash damage\n- Expensive upgrades',
        'tips': 'Place in central locations to cover the entire map.'
    },
    'recursive_function': {
        'name': 'Recursive Function',
        'role': 'Multi-Hit Specialist',
        'strengths': '- Hits enemies multiple times\n- Good pierce\n- Medium range',
        'weaknesses': '- Complex attack pattern\n- Moderate speed\n- Path dependent',
        'tips': 'Place near straight paths for maximum effectiveness.'
    },
    'async_processor': {
        'name': 'Async Processor',
        'role': 'Fast Attack Specialist',
        'strengths': '- Very fast attack speed\n- Can detect camo\n- Reliable damage',
        'weaknesses': '- Low damage per hit\n- Medium range\n- Higher cost',
        'tips': 'Great for dealing with fast enemies and swarms.'
    },
    'exception_handler': {
        'name': 'Exception Handler',
        'role': 'Area Damage',
        'strengths': '- Splash damage\n- High damage potential\n- Good against groups',
        'weaknesses': '- Slow attack speed\n- Limited range\n- Can miss fast targets',
        'tips': 'Use for grouped enemies and at choke points.'
    },
    'cache_freezer': {
        'name': 'Cache Freezer',
        'role': 'Crowd Control',
        'strengths': '- Slows enemies\n- Area effect\n- Support tower',
        'weaknesses': '- No direct damage\n- Short range\n- Some enemies immune',
        'tips': 'Combine with high damage towers for best results.'
    },
    'garbage_collector': {
        'name': 'Garbage Collector',
        'role': 'Debuff Specialist',
        'strengths': '- Permanent slow\n- Affects all types\n- Stackable effect',
        'weaknesses': '- Very low damage\n- Single target\n- Support focused',
        'tips': 'Place early in the track to maximize slow duration.'
    },
    'quantum_computer': {
        'name': 'Quantum Computer',
        'role': 'Super Tower',
        'strengths': '- Extremely fast attacks\n- High DPS\n- Large range',
        'weaknesses': '- Very expensive\n- High upgrade costs\n- Power hungry',
        'tips': 'Save up for late game. Worth the investment.'
    },
    'network_router': {
        'name': 'Network Router',
        'role': 'Support',
        'strengths': '- Buffs nearby towers\n- Multiple effects\n- Stackable buffs',
        'weaknesses': '- No direct damage\n- Expensive\n- Requires other towers',
        'tips': 'Place in areas with many other towers.'
    },
    'bitcoin_miner': {
        'name': 'Bitcoin Miner',
        'role': 'Income Generator',
        'strengths': '- Generates money\n- Self-sustaining\n- Long term value',
        'weaknesses': '- No attack ability\n- High initial cost\n- Takes time to profit',
        'tips': 'Build early for maximum profit over time.'
    },
    'stack_overflow': {
        'name': 'Stack Overflow',
        'role': 'Area Denial',
        'strengths': '- Persistent damage\n- Area control\n- Good backup defense',
        'weaknesses': '- Limited duration\n- Random targeting\n- Moderate cost',
        'tips': 'Use to protect end of track or create safe zones.'
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