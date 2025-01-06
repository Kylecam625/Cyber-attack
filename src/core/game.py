import pygame
import pygame_gui
from .settings import *
from ..managers.asset_manager import AssetManager
from ..managers.wave_manager import WaveManager
from ..entities.tower import Tower
import math
import os

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_speed = NORMAL_GAME_SPEED
        
        # Visual effect states
        self.path_pulse_value = 0
        self.particle_systems = []
        
        # Create surfaces for glow effects
        self.glow_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.path_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        
        # Game state - Initialize these first
        self.money = STARTING_MONEY
        self.lives = STARTING_LIVES
        self.wave = 1
        self.selected_tower = None  # For placement
        self.selected_existing_tower = None  # For showing stats
        
        # Initialize GUI with theme
        theme_path = os.path.join(os.path.dirname(__file__), 'theme.json')
        self.gui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), theme_path)
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
        # Main game panel with semi-transparent dark background
        panel_bg = pygame.Surface((250, WINDOW_HEIGHT))
        panel_bg.fill((40, 42, 54))
        panel_bg.set_alpha(230)
        
        self.game_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((WINDOW_WIDTH - 250, 0), (250, WINDOW_HEIGHT)),
            manager=self.gui_manager,
            object_id=pygame_gui.core.ObjectID(class_id='@panel')
        )
        
        # Tower selection buttons with descriptions
        y_offset = 10
        self.tower_buttons = {}  # Store buttons in a dict for easy access
        self.info_buttons = {}   # Store info buttons
        
        # Create scrollable container for tower buttons
        tower_container_height = min(WINDOW_HEIGHT - 300, len(TOWER_TYPES) * 45 + 20)  # Adjust height based on number of towers
        self.tower_container = pygame_gui.elements.UIScrollingContainer(
            relative_rect=pygame.Rect((5, y_offset), (240, tower_container_height)),
            manager=self.gui_manager,
            container=self.game_panel
        )
        
        button_y = 0
        for tower_type, stats in TOWER_TYPES.items():
            # Create button with proper name and cost on separate lines
            tower_info = TOWER_INFO[tower_type]
            name_text = tower_info['name']
            cost_text = f"${stats['cost']}"
            
            # Info button with improved tooltip
            info_text = (
                f"{tower_info['name']}\n\n"
                f"Role: {tower_info['role']}\n\n"
                f"Stats:\n"
                f"• Damage: {stats['damage']}\n"
                f"• Range: {stats['range']}\n"
                f"• Speed: {1/stats['cooldown']:.1f} shots/sec\n" if stats['cooldown'] > 0 else
                f"• Damage: {stats['damage']}\n"
                f"• Range: {stats['range']}\n"
                f"• Speed: Passive\n"
                f"• Cost: ${stats['cost']}\n\n"
                f"Strengths:\n{tower_info['strengths']}\n\n"
                f"Weaknesses:\n{tower_info['weaknesses']}\n\n"
                f"Tips:\n{tower_info['tips']}"
            )
            
            info_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((5, button_y + 5), (20, 30)),
                text='?',
                manager=self.gui_manager,
                container=self.tower_container,
                tool_tip_text=info_text,
                object_id=pygame_gui.core.ObjectID(
                    class_id='@info_buttons',
                    object_id=f'#info_button_{tower_type}'
                )
            )
            
            # Name label
            name_label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((30, button_y), (150, 20)),
                text=name_text,
                manager=self.gui_manager,
                container=self.tower_container
            )
            
            # Cost label
            cost_label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((30, button_y + 20), (150, 20)),
                text=cost_text,
                manager=self.gui_manager,
                container=self.tower_container
            )
            
            # Main tower button (invisible but clickable)
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((30, button_y), (200, 40)),
                text='',
                manager=self.gui_manager,
                container=self.tower_container,
                tool_tip_text=stats['description'],
                object_id=pygame_gui.core.ObjectID(
                    class_id='@tower_buttons',
                    object_id=f'#tower_button_{tower_type}'
                )
            )
            
            if self.money < stats['cost']:
                button.disable()
                name_label.set_text_alpha(128)
                cost_label.set_text_alpha(128)
            
            self.tower_buttons[tower_type] = button
            self.info_buttons[tower_type] = info_button
            button_y += 45
        
        # Update container to fit content
        self.tower_container.set_scrollable_area_dimensions((230, button_y + 10))
        
        # Stats panel with dark theme
        stats_y = y_offset + tower_container_height + 10
        self.stats_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((10, stats_y), (230, 100)),
            manager=self.gui_manager,
            container=self.game_panel,
            object_id=pygame_gui.core.ObjectID(
                class_id='@stats_panel',
                object_id='#main_stats_panel'
            )
        )
        
        # Stats labels with improved styling
        self.money_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 10), (210, 25)),
            text=f'Money: ${self.money}',
            manager=self.gui_manager,
            container=self.stats_panel,
            object_id=pygame_gui.core.ObjectID(
                class_id='@stats_labels'
            )
        )
        
        self.lives_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 40), (210, 25)),
            text=f'Lives: {self.lives}',
            manager=self.gui_manager,
            container=self.stats_panel,
            object_id=pygame_gui.core.ObjectID(
                class_id='@stats_labels'
            )
        )
        
        self.wave_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 70), (210, 25)),
            text=f'Wave: {self.wave}/{len(WAVE_CONFIGS)}',
            manager=self.gui_manager,
            container=self.stats_panel,
            object_id=pygame_gui.core.ObjectID(
                class_id='@stats_labels'
            )
        )
        
        # Game control buttons with consistent styling
        control_y = WINDOW_HEIGHT - 180
        
        # Sell button (initially hidden)
        self.sell_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, control_y), (230, 40)),
            text='Sell Tower',
            manager=self.gui_manager,
            container=self.game_panel,
            visible=False,
            object_id=pygame_gui.core.ObjectID(
                class_id='@control_buttons',
                object_id='#sell_button'
            )
        )
        
        # Start wave button
        self.start_wave_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, control_y + 45), (230, 40)),
            text='Start Wave',
            manager=self.gui_manager,
            container=self.game_panel,
            object_id=pygame_gui.core.ObjectID(
                class_id='@control_buttons',
                object_id='#start_wave_button'
            )
        )
        
        # Fast forward button
        self.fast_forward_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, control_y + 90), (230, 40)),
            text='Fast Forward (2x)',
            manager=self.gui_manager,
            container=self.game_panel,
            object_id=pygame_gui.core.ObjectID(
                class_id='@control_buttons',
                object_id='#fast_forward_button'
            )
        )
        
        # Create info panel (initially hidden)
        self.info_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((WINDOW_WIDTH//2 - 200, WINDOW_HEIGHT//2 - 200), (400, 400)),
            manager=self.gui_manager,
            visible=False,
            object_id=pygame_gui.core.ObjectID(class_id='@stats_panel')
        )
        
        # Close button for info panel
        self.info_close_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((360, 10), (30, 30)),
            text='X',
            manager=self.gui_manager,
            container=self.info_panel,
            visible=False,
            object_id=pygame_gui.core.ObjectID(class_id='@control_buttons')
        )
        
        # Info text box
        self.info_textbox = pygame_gui.elements.UITextBox(
            html_text="",
            relative_rect=pygame.Rect((10, 50), (380, 340)),
            manager=self.gui_manager,
            container=self.info_panel,
            visible=False
        )
        
        # Wave info at the top
        self.wave_info_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((10, 10), (300, 50)),
            manager=self.gui_manager,
            object_id=pygame_gui.core.ObjectID(class_id='@stats_panel')
        )
        
        self.wave_info_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 10), (280, 30)),
            text=f'Wave {self.wave}/{len(WAVE_CONFIGS)}',
            manager=self.gui_manager,
            container=self.wave_info_panel,
            object_id=pygame_gui.core.ObjectID(class_id='@stats_labels')
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
        # In BTD, end of round bonus is typically $100 for early rounds,
        # increasing by small amounts each round
        bonus = 100 + (self.wave * 10)  # Start at 100, increase by 10 per wave
        self.money += bonus
        
        # Enable start wave button if not on last wave
        if self.wave < len(WAVE_CONFIGS):
            self.start_wave_button.enable()
            self.start_wave_button.set_text('Start Wave')  # Reset button text
        else:
            self.start_wave_button.disable()
            self.start_wave_button.set_text('Game Complete!')
        
        # Update tower buttons with new money amount
        self.update_tower_buttons()
    
    def handle_events(self):
        time_delta = self.clock.tick(FPS)/1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.start_wave_button:
                        if self.wave_manager.start_wave():
                            self.start_wave_button.disable()
                            self.start_wave_button.set_text('Wave in Progress...')
                            self.wave += 1  # Increment wave counter when wave starts
                            self.wave_info_label.set_text(f'Wave {self.wave}/{len(WAVE_CONFIGS)}')
                    elif event.ui_element == self.sell_button and self.selected_existing_tower:
                        self.sell_tower(self.selected_existing_tower)
                    elif event.ui_element == self.fast_forward_button:
                        # Toggle game speed
                        if self.game_speed == NORMAL_GAME_SPEED:
                            self.game_speed = FAST_FORWARD_SPEED
                            self.fast_forward_button.set_text('Normal Speed (1x)')
                        else:
                            self.game_speed = NORMAL_GAME_SPEED
                            self.fast_forward_button.set_text('Fast Forward (2x)')
                    elif event.ui_element == self.info_close_button:
                        self.info_panel.hide()
                        self.info_close_button.hide()
                        self.info_textbox.hide()
                    elif event.ui_element in self.info_buttons.values():
                        # Show info panel for the clicked tower
                        for tower_type, info_btn in self.info_buttons.items():
                            if event.ui_element == info_btn:
                                self.show_tower_info(tower_type)
                                break
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
                    self.sell_button.hide()
                elif event.button == 1:  # Left click
                    if not self.game_panel.get_abs_rect().collidepoint(event.pos):
                        if self.selected_tower:  # Placing new tower
                            self.handle_mouse_click(event.pos)
                        else:  # Selecting existing tower
                            self.handle_tower_selection(event.pos)
            
            self.gui_manager.process_events(event)
        
        # Apply game speed to time_delta for game logic updates
        scaled_time_delta = time_delta * self.game_speed
        
        # Update game state with scaled time
        self.wave_manager.update(scaled_time_delta)
        for enemy in self.enemies:
            enemy.update(scaled_time_delta)
        for tower in self.towers:
            tower.update(self.enemies, self.projectiles, scaled_time_delta)
        for projectile in self.projectiles:
            projectile.update(scaled_time_delta)
        
        # Check projectile hits
        for projectile in self.projectiles:
            for enemy in self.enemies:
                if projectile.rect.colliderect(enemy.rect):
                    if enemy.take_damage(projectile.damage):
                        # Find the tower that shot this projectile
                        for tower in self.towers:
                            if tower.rect.center == projectile.initial_pos:
                                tower.enemies_defeated += 1
                                tower.damage_dealt += enemy.stats['health']
                                break
                        self.money += enemy.reward
                        enemy.kill()
                    projectile.kill()
                    break
        
        # Check if enemies reached the end
        for enemy in self.enemies:
            if enemy.reached_end or enemy.path_index >= len(enemy.path_points) - 1:
                self.lives -= enemy.stats['damage']
                enemy.kill()
        
        # Update UI with unscaled time (UI should remain at normal speed)
        self.gui_manager.update(time_delta)
        self.money_label.set_text(f'Money: ${self.money}')
        self.lives_label.set_text(f'Lives: {self.lives}')
        self.wave_label.set_text(f'Wave: {self.wave}/{len(WAVE_CONFIGS)}')
        
        # Update tower buttons based on money
        self.update_tower_buttons()
    
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
            self.sell_button.hide()
        
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
            # Show sell button with sell price
            sell_price = int(TOWER_TYPES[clicked_tower.type]['cost'] * 0.7)  # 70% refund
            self.sell_button.set_text(f'Sell Tower (${sell_price})')
            self.sell_button.show()
        else:
            self.sell_button.hide()
    
    def sell_tower(self, tower):
        # Calculate refund (70% of original cost)
        refund = int(TOWER_TYPES[tower.type]['cost'] * 0.7)
        self.money += refund
        
        # Get grid position
        grid_x = tower.rect.centerx // TILE_SIZE
        grid_y = tower.rect.centery // TILE_SIZE
        
        # Clear grid position
        self.grid[grid_y][grid_x] = 0
        
        # Remove tower
        tower.kill()
        self.selected_existing_tower = None
        self.sell_button.hide()
        
        # Update tower buttons
        self.update_tower_buttons()
    
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
        # Clear screen and surfaces
        self.screen.fill(BLACK)
        self.glow_surface.fill((0, 0, 0, 0))
        
        # Draw grid with tech effect
        self.draw_tech_grid()
        
        # Draw tower glows
        if GLOW_EFFECT:
            for tower in self.towers:
                glow_color = TOWER_GLOW_COLORS[tower.type]
                glow_surf = pygame.Surface((GLOW_RADIUS * 2, GLOW_RADIUS * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, glow_color, 
                                 (GLOW_RADIUS, GLOW_RADIUS), GLOW_RADIUS)
                self.glow_surface.blit(glow_surf, 
                                     (tower.rect.centerx - GLOW_RADIUS,
                                      tower.rect.centery - GLOW_RADIUS),
                                     special_flags=pygame.BLEND_ALPHA_SDL2)
        
        # Draw tower ranges (only for selected towers)
        for tower in self.towers:
            tower.draw_range(self.screen)
        
        # Draw game objects
        self.towers.draw(self.screen)
        self.enemies.draw(self.screen)
        self.projectiles.draw(self.screen)
        
        # Draw enemy health bars and glows
        for enemy in self.enemies:
            if GLOW_EFFECT:
                glow_color = ENEMY_GLOW_COLORS[enemy.type]
                glow_surf = pygame.Surface((GLOW_RADIUS * 2, GLOW_RADIUS * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, glow_color, 
                                 (GLOW_RADIUS, GLOW_RADIUS), GLOW_RADIUS)
                self.glow_surface.blit(glow_surf, 
                                     (enemy.rect.centerx - GLOW_RADIUS,
                                      enemy.rect.centery - GLOW_RADIUS),
                                     special_flags=pygame.BLEND_ALPHA_SDL2)
            enemy.draw_health_bar(self.screen)
        
        # Apply glow surface
        self.screen.blit(self.glow_surface, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
        
        # Draw tower placement preview with glow
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
            
            # Draw range preview with glow
            range_radius = TOWER_TYPES[self.selected_tower]['range']
            if GLOW_EFFECT:
                glow_surf = pygame.Surface((range_radius * 2 + 20, range_radius * 2 + 20), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (*color, 30), 
                                 (range_radius + 10, range_radius + 10), range_radius)
                self.screen.blit(glow_surf, 
                               (grid_x * TILE_SIZE + TILE_SIZE // 2 - range_radius - 10,
                                grid_y * TILE_SIZE + TILE_SIZE // 2 - range_radius - 10),
                               special_flags=pygame.BLEND_ALPHA_SDL2)
            pygame.draw.circle(self.screen, color, 
                             (grid_x * TILE_SIZE + TILE_SIZE // 2,
                              grid_y * TILE_SIZE + TILE_SIZE // 2),
                             range_radius, 2)
        
        # Draw selected tower stats with improved styling
        if self.selected_existing_tower:
            self.draw_tower_stats(self.selected_existing_tower)
        
        # Draw GUI
        self.gui_manager.draw_ui(self.screen)
        pygame.display.flip()
    
    def draw_tower_stats(self, tower):
        # Create a stats box with improved styling
        stats_text = tower.get_stats_text()
        line_height = 24  # Increased line height
        padding = 15     # Increased padding
        box_height = len(stats_text) * line_height + padding * 2
        box_width = 220  # Increased width
        
        # Position the box near but not on top of the tower
        box_x = min(tower.rect.centerx + 20, WINDOW_WIDTH - box_width - 260)
        box_y = min(tower.rect.centery, WINDOW_HEIGHT - box_height)
        
        # Draw semi-transparent background with border
        stats_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(stats_surface, (*UI_BACKGROUND, 230), 
                        (0, 0, box_width, box_height))
        pygame.draw.rect(stats_surface, (*UI_ACCENT, 255), 
                        (0, 0, box_width, box_height), 2)
        self.screen.blit(stats_surface, (box_x, box_y))
        
        # Draw stats text with improved font
        font = pygame.font.Font(None, 26)  # Increased font size
        for i, text in enumerate(stats_text):
            text_surface = font.render(text, True, UI_TEXT)
            self.screen.blit(text_surface, 
                           (box_x + padding, 
                            box_y + padding + i * line_height))
    
    def draw_tech_grid(self):
        # Create surface for grid
        grid_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        
        # Update path pulse
        self.path_pulse_value = (self.path_pulse_value + PATH_PULSE_SPEED) % (2 * math.pi)
        pulse_alpha = int((PATH_PULSE_MAX - PATH_PULSE_MIN) * 
                         (math.sin(self.path_pulse_value) * 0.5 + 0.5) + PATH_PULSE_MIN * 255)
        
        # Draw base grid with tech effect
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, 
                                 TILE_SIZE, TILE_SIZE)
                
                # Draw path with tech effect and glow
                if self.grid[y][x] == 2:
                    # Draw base path
                    path_color = (*BROWN, pulse_alpha)
                    pygame.draw.rect(grid_surface, path_color, rect)
                    
                    # Add circuit pattern
                    pygame.draw.line(grid_surface, (*BROWN, pulse_alpha),
                                   (rect.left + 2, rect.centery),
                                   (rect.right - 2, rect.centery), 2)
                    pygame.draw.line(grid_surface, (*BROWN, pulse_alpha),
                                   (rect.centerx, rect.top + 2),
                                   (rect.centerx, rect.bottom - 2), 2)
                    
                    # Add glow effect
                    if PATH_GLOW:
                        glow_surf = pygame.Surface((TILE_SIZE * 2, TILE_SIZE * 2), pygame.SRCALPHA)
                        pygame.draw.rect(glow_surf, (*BROWN, 30), 
                                       (TILE_SIZE//2, TILE_SIZE//2, TILE_SIZE, TILE_SIZE))
                        grid_surface.blit(glow_surf, 
                                        (rect.x - TILE_SIZE//2, rect.y - TILE_SIZE//2),
                                        special_flags=pygame.BLEND_ALPHA_SDL2)
                
                # Draw subtle grid lines
                pygame.draw.rect(grid_surface, (*GRID_LINE_COLOR, int(255 * GRID_OPACITY)), 
                               rect, 1)
        
        # Draw hover effect
        if self.selected_tower:
            mouse_pos = pygame.mouse.get_pos()
            grid_x = mouse_pos[0] // TILE_SIZE
            grid_y = mouse_pos[1] // TILE_SIZE
            hover_rect = pygame.Rect(grid_x * TILE_SIZE, grid_y * TILE_SIZE,
                                   TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(grid_surface, GRID_HOVER_COLOR, hover_rect)
        
        self.screen.blit(grid_surface, (0, 0))
    
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
    
    def show_tower_info(self, tower_type):
        tower_info = TOWER_INFO[tower_type]
        stats = TOWER_TYPES[tower_type]
        
        # Format speed text
        speed_text = 'Passive' if stats['cooldown'] == 0 else f'{1/stats["cooldown"]:.1f} shots/sec'
        
        # Format strengths, weaknesses, and tips with proper HTML line breaks
        strengths = tower_info['strengths'].replace('\n', '<br>')
        weaknesses = tower_info['weaknesses'].replace('\n', '<br>')
        tips = tower_info['tips'].replace('\n', '<br>')
        
        # Format info text with HTML for better styling
        info_text = (
            f'<b><font size=5>{tower_info["name"]}</font></b><br><br>'
            f'<b>Role:</b> {tower_info["role"]}<br><br>'
            f'<b>Stats:</b><br>'
            f'• Damage: {stats["damage"]}<br>'
            f'• Range: {stats["range"]}<br>'
            f'• Speed: {speed_text}<br>'
            f'• Cost: ${stats["cost"]}<br><br>'
            f'<b>Strengths:</b><br>'
            f'{strengths}<br><br>'
            f'<b>Weaknesses:</b><br>'
            f'{weaknesses}<br><br>'
            f'<b>Tips:</b><br>'
            f'{tips}'
        )
        
        # Update and show info panel
        self.info_textbox.html_text = info_text
        self.info_textbox.rebuild()
        self.info_panel.show()
        self.info_close_button.show()
        self.info_textbox.show() 