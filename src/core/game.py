import pygame
import pygame_gui
from .settings import *
from ..managers.asset_manager import AssetManager
from ..managers.wave_manager import WaveManager
from ..entities.tower import Tower

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game state - Initialize these first
        self.money = STARTING_MONEY
        self.lives = STARTING_LIVES
        self.wave = 1
        self.selected_tower = None  # For placement
        self.selected_existing_tower = None  # For showing stats
        
        # Initialize GUI after game state
        self.gui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.setup_gui()
        
        # Initialize managers
        self.asset_manager = AssetManager()
        self.wave_manager = WaveManager(self)
        
        # Initialize sprite groups
        self.towers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        
        # Create path points
        self.path_points = self.generate_path_points()
        
        # Create game map grid (0: empty, 1: tower, 2: path)
        self.grid = [[0 for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
        self.mark_path_on_grid()
    
    def setup_gui(self):
        # Main game panel
        self.game_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((WINDOW_WIDTH - 250, 0), (250, WINDOW_HEIGHT)),
            manager=self.gui_manager
        )
        
        # Tower selection buttons with descriptions
        y_offset = 10
        self.tower_buttons = {}  # Store buttons in a dict for easy access
        
        for tower_type, stats in TOWER_TYPES.items():
            # Create button with cost
            cost_text = f"{tower_type.title()} (${stats['cost']})"
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((10, y_offset), (230, 50)),
                text=cost_text,
                manager=self.gui_manager,
                container=self.game_panel,
                tool_tip_text=stats['description']  # Show description on hover
            )
            
            if self.money < stats['cost']:
                button.disable()  # Disable if can't afford
            
            self.tower_buttons[tower_type] = button
            y_offset += 60  # Reduced spacing
        
        # Stats panel
        self.stats_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((10, y_offset), (230, 120)),
            manager=self.gui_manager,
            container=self.game_panel
        )
        
        # Stats labels
        self.money_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 10), (210, 30)),
            text=f'Money: ${self.money}',
            manager=self.gui_manager,
            container=self.stats_panel
        )
        
        self.lives_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 40), (210, 30)),
            text=f'Lives: {self.lives}',
            manager=self.gui_manager,
            container=self.stats_panel
        )
        
        self.wave_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 70), (210, 30)),
            text=f'Wave: {self.wave}/{len(WAVE_CONFIGS)}',
            manager=self.gui_manager,
            container=self.stats_panel
        )
        
        # Start wave button
        self.start_wave_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, WINDOW_HEIGHT - 150), (230, 50)),
            text='Start Wave',
            manager=self.gui_manager,
            container=self.game_panel
        )
    
    def generate_path_points(self):
        """Generate all points along the path for smooth enemy movement"""
        points = []
        for i in range(len(PATH_WAYPOINTS) - 1):
            start = PATH_WAYPOINTS[i]
            end = PATH_WAYPOINTS[i + 1]
            
            # Generate points between waypoints
            if start[0] == end[0]:  # Vertical line
                step = 1 if end[1] > start[1] else -1
                for y in range(start[1], end[1] + step, step):
                    if 0 <= y < GRID_HEIGHT and 0 <= start[0] < GRID_WIDTH:
                        points.append((start[0], y))
            else:  # Horizontal line
                step = 1 if end[0] > start[0] else -1
                for x in range(start[0], end[0] + step, step):
                    if 0 <= x < GRID_WIDTH and 0 <= start[1] < GRID_HEIGHT:
                        points.append((x, start[1]))
        
        return points
    
    def mark_path_on_grid(self):
        """Mark the path on the grid"""
        for x, y in self.path_points:
            if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]):
                self.grid[y][x] = 2
    
    def spawn_enemy(self, enemy_type):
        from ..entities.enemy import Enemy
        # Get current wave config
        wave_config = WAVE_CONFIGS[self.wave - 1]
        
        # Convert grid coordinates to pixels for starting position
        start_pos = (PATH_WAYPOINTS[0][0] * TILE_SIZE + TILE_SIZE // 2,
                    PATH_WAYPOINTS[0][1] * TILE_SIZE + TILE_SIZE // 2)
        
        # Create enemy with wave scaling
        enemy = Enemy(enemy_type, self.path_points, {
            'health_scale': wave_config['health_scale'],
            'speed_scale': wave_config['speed_scale']
        })
        self.enemies.add(enemy)
    
    def wave_completed(self):
        # Give bonus money for completing wave
        bonus = 100 + (self.wave * 50)
        self.money += bonus
        
        # Enable start wave button if not on last wave
        if self.wave < len(WAVE_CONFIGS):
            self.start_wave_button.enable()
        
        # Update tower buttons with new money amount
        self.update_tower_buttons()
    
    def handle_events(self):
        time_delta = self.clock.tick(FPS)/1000.0
        
        # Debug info at start of frame
        print("\n--- New Frame ---")
        print(f"Current wave: {self.wave}")
        print(f"Active towers: {len(self.towers)}")
        print(f"Active enemies: {len(self.enemies)}")
        print(f"Active projectiles: {len(self.projectiles)}")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.start_wave_button:
                        if self.wave_manager.start_wave():
                            self.start_wave_button.disable()
                            self.wave += 1  # Increment wave counter
                    else:
                        # Check if tower button was pressed
                        for tower_type, button in self.tower_buttons.items():
                            if event.ui_element == button:
                                # Only select if we can afford it
                                if self.money >= TOWER_TYPES[tower_type]['cost']:
                                    self.selected_tower = tower_type
                                break
            
            # Right click to cancel tower placement
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  # Right click
                    self.selected_tower = None
                    self.selected_existing_tower = None
                elif event.button == 1:  # Left click
                    if not self.game_panel.get_abs_rect().collidepoint(event.pos):
                        if self.selected_tower:  # Placing new tower
                            self.handle_mouse_click(event.pos)
                        else:  # Selecting existing tower
                            self.handle_tower_selection(event.pos)
            
            self.gui_manager.process_events(event)
        
        # Update game state
        print("\nUpdating wave manager...")
        self.wave_manager.update()
        
        print("\nUpdating game objects...")
        self.enemies.update()
        for tower in self.towers:  # Update towers individually for better debugging
            tower.update(self.enemies, self.projectiles)
        self.projectiles.update()
        
        # Debug info after updates
        print("\nAfter updates:")
        print(f"Enemies remaining: {len(self.enemies)}")
        print(f"Active projectiles: {len(self.projectiles)}")
        
        # Check projectile hits
        for projectile in self.projectiles:
            for enemy in self.enemies:
                if projectile.rect.colliderect(enemy.rect):
                    if enemy.take_damage(projectile.damage):
                        # Find the tower that shot this projectile
                        for tower in self.towers:
                            if tower.rect.center == projectile.initial_pos:  # Add initial_pos to Projectile class
                                tower.enemies_defeated += 1
                                tower.damage_dealt += enemy.stats['health']  # Add full health as damage
                                break
                        self.money += enemy.reward
                        enemy.kill()
                    projectile.kill()
                    break
        
        # Check if enemies reached the end
        for enemy in self.enemies:
            if enemy.path_index >= len(enemy.path_points) - 1:
                self.lives -= enemy.stats['damage']
                enemy.kill()
        
        # Update UI
        self.gui_manager.update(time_delta)
        self.money_label.set_text(f'Money: ${self.money}')
        self.lives_label.set_text(f'Lives: {self.lives}')
        self.wave_label.set_text(f'Wave: {self.wave}/{len(WAVE_CONFIGS)}')
        
        # Update tower buttons based on money
        self.update_tower_buttons()
        
        # After projectile hits check:
        print(f"Active projectiles after update: {len(self.projectiles)}")
    
    def handle_mouse_click(self, pos):
        # Only handle clicks if a tower is selected
        if not self.selected_tower:
            return
            
        # Convert mouse position to grid coordinates
        grid_x = pos[0] // TILE_SIZE
        grid_y = pos[1] // TILE_SIZE
        
        # Check if we can place a tower here
        if (grid_y < len(self.grid) and grid_x < len(self.grid[0]) and
            self.money >= TOWER_TYPES[self.selected_tower]['cost'] and 
            self.grid[grid_y][grid_x] == 0):
            # Place tower
            tower = Tower(self.selected_tower, 
                         (grid_x * TILE_SIZE + TILE_SIZE // 2, 
                          grid_y * TILE_SIZE + TILE_SIZE // 2))
            self.towers.add(tower)
            self.money -= TOWER_TYPES[self.selected_tower]['cost']
            self.grid[grid_y][grid_x] = 1
            self.selected_tower = None  # Deselect tower after placing
    
    def handle_tower_selection(self, pos):
        # Deselect previously selected tower
        if self.selected_existing_tower:
            self.selected_existing_tower.selected = False
        
        # Check if clicked on a tower
        clicked_tower = None
        for tower in self.towers:
            if tower.rect.collidepoint(pos):
                clicked_tower = tower
                break
        
        # Update selection
        self.selected_existing_tower = clicked_tower
        if clicked_tower:
            clicked_tower.selected = True
    
    def draw_grid(self):
        # Draw the base grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, 
                                 TILE_SIZE, TILE_SIZE)
                
                # Draw path
                if self.grid[y][x] == 2:
                    pygame.draw.rect(self.screen, BROWN, rect)
                
                # Draw grid lines
                pygame.draw.rect(self.screen, GRAY, rect, 1)
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw grid with tech effect
        self.draw_tech_grid()
        
        # Draw tower ranges (only for selected towers)
        for tower in self.towers:
            tower.draw_range(self.screen)
        
        # Draw game objects
        self.towers.draw(self.screen)
        self.enemies.draw(self.screen)
        self.projectiles.draw(self.screen)
        
        # Draw enemy health bars
        for enemy in self.enemies:
            enemy.draw_health_bar(self.screen)
        
        # Draw tower placement preview
        if self.selected_tower:
            mouse_pos = pygame.mouse.get_pos()
            grid_x = mouse_pos[0] // TILE_SIZE
            grid_y = mouse_pos[1] // TILE_SIZE
            
            # Show where tower would be placed
            preview_rect = pygame.Rect(
                grid_x * TILE_SIZE, grid_y * TILE_SIZE,
                TILE_SIZE, TILE_SIZE
            )
            
            # Color based on whether placement is valid
            can_place = (grid_y < len(self.grid) and grid_x < len(self.grid[0]) and
                        self.money >= TOWER_TYPES[self.selected_tower]['cost'] and
                        self.grid[grid_y][grid_x] == 0 and
                        not self.game_panel.get_abs_rect().collidepoint(mouse_pos))
            
            color = GREEN if can_place else RED
            pygame.draw.rect(self.screen, color, preview_rect, 2)
            
            # Draw range preview
            range_radius = TOWER_TYPES[self.selected_tower]['range']
            pygame.draw.circle(self.screen, color, 
                             (grid_x * TILE_SIZE + TILE_SIZE // 2,
                              grid_y * TILE_SIZE + TILE_SIZE // 2),
                             range_radius, 1)
        
        # Draw selected tower stats
        if self.selected_existing_tower:
            self.draw_tower_stats(self.selected_existing_tower)
        
        # Draw GUI
        self.gui_manager.draw_ui(self.screen)
        pygame.display.flip()
    
    def draw_tower_stats(self, tower):
        # Create a stats box
        stats_text = tower.get_stats_text()
        line_height = 20
        box_height = len(stats_text) * line_height + 20
        box_width = 200
        
        # Position the box near but not on top of the tower
        box_x = min(tower.rect.centerx + 20, WINDOW_WIDTH - box_width - 260)  # Avoid UI panel
        box_y = min(tower.rect.centery, WINDOW_HEIGHT - box_height)
        
        # Draw semi-transparent background
        stats_surface = pygame.Surface((box_width, box_height))
        stats_surface.fill(BLACK)
        stats_surface.set_alpha(200)
        self.screen.blit(stats_surface, (box_x, box_y))
        
        # Draw stats text
        font = pygame.font.Font(None, 24)
        for i, text in enumerate(stats_text):
            text_surface = font.render(text, True, WHITE)
            self.screen.blit(text_surface, (box_x + 10, box_y + 10 + i * line_height))
    
    def draw_tech_grid(self):
        # Draw base grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, 
                                 TILE_SIZE, TILE_SIZE)
                
                # Draw path with tech effect
                if self.grid[y][x] == 2:
                    pygame.draw.rect(self.screen, BROWN, rect)
                    # Add circuit pattern
                    pygame.draw.line(self.screen, (*BROWN, 150),
                                   (rect.left + 2, rect.centery),
                                   (rect.right - 2, rect.centery), 1)
                    pygame.draw.line(self.screen, (*BROWN, 150),
                                   (rect.centerx, rect.top + 2),
                                   (rect.centerx, rect.bottom - 2), 1)
                
                # Draw subtle grid lines
                alpha_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                pygame.draw.rect(alpha_surface, (100, 100, 100, 30), 
                               (0, 0, TILE_SIZE, TILE_SIZE), 1)
                self.screen.blit(alpha_surface, rect)
    
    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
        
        pygame.quit() 
    
    def update_tower_buttons(self):
        """Enable/disable tower buttons based on money"""
        for tower_type, button in self.tower_buttons.items():
            if self.money >= TOWER_TYPES[tower_type]['cost']:
                button.enable()
            else:
                button.disable() 