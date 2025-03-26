import pygame as pg

from src.sokoban import Sokoban, movimientos


class SokobanVisualizer(Sokoban):
    def __init__(self, filename):
        super().__init__(filename)

        self.window_size = (600, 600)

        pg.init()

        self.height_size = self.window_size[1] // len(self.map)
        self.width_size = self.window_size[0] // len(self.map[0])

        self.last_update = 0

    def apply_move(self, move):
        dx, dy = movimientos[move]
        new_player = (self.player[0] + dx, self.player[1] + dy)

        if new_player in self.boxes:
            new_box = (new_player[0] + dx, self.player[1] + dy)
            self.boxes.remove(new_player)
            self.boxes.add(new_box)

        self.player = new_player

    def print_map(self):
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                pos = (x, y)
                rect = pg.Rect(x * self.width_size, y * self.height_size, self.width_size, self.height_size)
                self.screen.blit(pg.transform.scale(self.floor_sprite, (self.width_size, self.height_size)), rect)

                if pos == self.player:
                    self.screen.blit(pg.transform.scale(self.player_sprite, (self.width_size, self.height_size)), rect)

                elif pos in self.boxes:
                    if pos in self.targets:
                        self.screen.blit(pg.transform.scale(self.box_target_sprite, (self.width_size, self.height_size)), rect)
                    else:
                        self.screen.blit(pg.transform.scale(self.box_sprite, (self.width_size, self.height_size)), rect)

                elif pos in self.targets:
                    self.screen.blit(pg.transform.scale(self.target_sprite, (self.width_size, self.height_size)), rect)

                elif cell == "#":
                    self.screen.blit(pg.transform.scale(self.wall_sprite, (self.width_size, self.height_size)), rect)

        pg.display.flip()

    def play_solution(self, solution):
        self.screen = pg.display.set_mode(self.window_size)
        self.clock = pg.time.Clock()

        pg.display.set_caption("Sokoban simulation (Running...)")

        # Load sprites
        self.box_sprite = pg.image.load("assets/box.png").convert_alpha()
        self.box_target_sprite = pg.image.load("assets/box_target.png").convert_alpha()
        self.wall_sprite = pg.image.load("assets/wall.png")
        self.floor_sprite = pg.image.load("assets/floor.png")
        self.player_sprite = pg.image.load("assets/player.png").convert_alpha()
        self.target_sprite = pg.image.load("assets/target.png").convert_alpha()

        # Display initial state
        self.print_map()
        
        state_index = 0
        running = True
        paused = False
        
        # Get solution states
        solution_states = solution.get("path")
        total_states = solution.get("steps")

        while running:
            self.clock.tick(60)  # Run at 60 FPS

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        paused = True
                        pg.display.set_caption("Sokoban simulation (Paused...)")

                        state_index = 0
                        # Reset to initial state
                        initial_state = solution_states[0]
                        self.player = initial_state.get("player")
                        self.boxes = set(tuple(box) for box in initial_state.get("boxes"))
                        self.print_map()

                    if event.key == pg.K_SPACE:
                        paused = not paused
                        pg.display.set_caption(f"Sokoban simulation ({'Paused' if paused else 'Running'}...)")

                    if event.key == pg.K_RIGHT:
                        paused = True
                        pg.display.set_caption("Sokoban simulation (Paused...)")

                        if state_index < total_states - 1:
                            state_index += 1
                            current_state = solution_states[state_index]
                            self.player = current_state.get("player")
                            self.boxes = current_state.get("boxes")
                            self.print_map()

                    if event.key == pg.K_LEFT:
                        paused = True
                        pg.display.set_caption("Sokoban simulation (Paused...)")

                        if state_index > 0:
                            state_index -= 1
                            current_state = solution_states[state_index]
                            self.player = current_state.get("player")
                            self.boxes = current_state.get("boxes")
                            self.print_map()

            if not paused and state_index < total_states - 1:
                if pg.time.get_ticks() - self.last_update >= 200:  # Update simulation at 5 steps per second
                    state_index += 1
                    current_state = solution_states[state_index]
                    
                    # Update player and boxes directly from state data
                    self.player = current_state.get("player")
                    self.boxes = current_state.get("boxes")
                    
                    self.print_map()
                    self.last_update = pg.time.get_ticks()
