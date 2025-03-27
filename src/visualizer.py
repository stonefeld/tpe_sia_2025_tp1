import pygame as pg


class SokobanVisualizer:
    def __init__(self, solution):
        self.window_size = (600, 600)

        self.map = solution.get("map")
        self.targets = set((target.get("x"), target.get("y")) for target in solution.get("targets"))
        self.steps = solution.get("steps")
        self.path = solution.get("path")

        self.height_size = self.window_size[1] // len(self.map)
        self.width_size = self.window_size[0] // len(self.map[0])

        self.state_idx = 0
        self.last_update = 0

        pg.init()
        self.screen = pg.display.set_mode(self.window_size)
        self.clock = pg.time.Clock()

        self.box_sprite = pg.image.load("assets/box.png").convert_alpha()
        self.box_target_sprite = pg.image.load("assets/box_target.png").convert_alpha()
        self.wall_sprite = pg.image.load("assets/wall.png")
        self.floor_sprite = pg.image.load("assets/floor.png")
        self.player_sprite = pg.image.load("assets/player.png").convert_alpha()
        self.target_sprite = pg.image.load("assets/target.png").convert_alpha()

    def print_map(self):
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                pos = (x, y)
                rect = pg.Rect(x * self.width_size, y * self.height_size, self.width_size, self.height_size)

                if cell == "#":
                    self.screen.blit(pg.transform.scale(self.wall_sprite, (self.width_size, self.height_size)), rect)
                else:
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

        pg.display.flip()

    def play_solution(self):
        self.state_idx = 0
        self.state_and_render()

        running = True
        paused = False

        while running:
            self.clock.tick(60)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        paused = True
                        self.state_idx = 0
                        self.state_and_render()

                    if event.key == pg.K_SPACE:
                        paused = not paused

                    if event.key == pg.K_RIGHT:
                        paused = True
                        if self.state_idx < self.steps:
                            self.state_idx += 1
                            self.state_and_render()

                    if event.key == pg.K_LEFT:
                        paused = True
                        if self.state_idx > 0:
                            self.state_idx -= 1
                            self.state_and_render()

            if not paused and self.state_idx < self.steps:
                if pg.time.get_ticks() - self.last_update >= 200:
                    self.state_idx += 1
                    self.state_and_render()
                    self.last_update = pg.time.get_ticks()

    def state_and_render(self):
        state = self.path[self.state_idx]

        pg.display.set_caption(f"Sokoban visualizer ({self.state_idx}/{self.steps})")

        self.boxes = set((box.get("x"), box.get("y")) for box in state.get("boxes"))
        self.player = (state.get("player").get("x"), state.get("player").get("y"))

        self.print_map()
