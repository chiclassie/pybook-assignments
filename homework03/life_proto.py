import random
import typing as tp

import pygame
from pygame import QUIT
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 12
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.
        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.
        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.
        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if not randomize:
            return [[0 for i in range(0, self.cell_width)] for k in range(0, self.cell_height)]
        return [
            [random.randint(0, 1) for i in range(0, self.cell_width)]
            for k in range(0, self.cell_height)
        ]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        y = self.height
        for i in range(0, self.cell_height):
            x = 0
            y = y - self.cell_size
            for k in range(0, self.cell_width):
                if self.grid[i][k] == 0:
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

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.
        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.
        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.
        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neighbours = []

        row, col = cell

        for i in range(row - 1, row + 2):
            for k in range(col - 1, col + 2):
                if ((i == row) & (k == col)) or not (
                    0 <= k <= self.cell_width - 1 and 0 <= i <= self.cell_height - 1
                ):
                    continue
                neighbours.append(self.grid[i][k])

        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        next_generation_grid = self.create_grid(randomize=False)

        for i in range(0, self.cell_height):
            for k in range(0, self.cell_width):
                n_neighbours = sum(self.get_neighbours((i, k)))
                is_alive = self.grid[i][k] == 1
                if 2 <= n_neighbours <= 3 and is_alive:
                    next_generation_grid[i][k] = 1
                elif n_neighbours == 3 and not is_alive:
                    next_generation_grid[i][k] = 1
        return next_generation_grid


if __name__ == "__main__":
    game = GameOfLife(320, 240, 40)
    game.run()
