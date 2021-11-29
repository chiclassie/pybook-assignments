import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 7) -> None:
        super().__init__(life)
        self.speed = speed
        self.cell_size = cell_size
        self.screen = pygame.display.set_mode(
            (self.life.cols * self.cell_size, self.life.rows * self.cell_size)
        )
        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size

    def draw_lines(self) -> None:
        # Copy from previous assignment
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        # Copy from previous assignment
        y = self.height
        for i in range(self.life.rows):
            x = 0
            y -= self.cell_size
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 0:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (x + 1, y + 1, self.cell_size - 1, self.cell_size - 1),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (x + 1, y + 1, self.cell_size - 1, self.cell_size - 1),
                    )
                x += self.cell_size

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        paused = False
        draw = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    paused = not paused

            self.draw_lines()

            if paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        paused = not paused

                pressed = pygame.mouse.get_pressed(3)
                if pressed[0]:
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // self.cell_size
                    row = self.life.rows - pos[1] // self.cell_size - 1
                    if self.life.curr_generation[row][col]:
                        self.life.curr_generation[row][col] = 0
                    else:
                        self.life.curr_generation[row][col] = 1
                    self.draw_grid()
                    pygame.display.flip()

            else:
                self.life.step()
                self.draw_grid()
                if (not (self.life.is_changing)) or (not (self.life.is_max_generations_exceeded)):
                    running = False

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    gof = GameOfLife((10, 10))
    game = GUI(gof, 40, 10)
    game.run()
