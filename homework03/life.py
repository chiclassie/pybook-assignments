import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        if not randomize:
            return [[0 for i in range(0, self.cols)] for j in range(0, self.rows)]
        return [[random.randint(0, 1) for i in range(0, self.cols)] for j in range(0, self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment

        neighbours = []

        row, col = cell

        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if ((i == row) & (j == col)) or not (
                    0 <= j <= self.cols - 1 and 0 <= i <= self.rows - 1
                ):
                    continue
                neighbours.append(self.curr_generation[i][j])

        return neighbours

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment

        next_generation_grid = self.create_grid(randomize=False)

        for i in range(0, self.rows):
            for j in range(0, self.cols):
                n_neighbours = sum(self.get_neighbours((i, j)))
                is_alive = self.curr_generation[i][j] == 1
                if 2 <= n_neighbours <= 3 and is_alive:
                    next_generation_grid[i][j] = 1
                elif n_neighbours == 3 and not is_alive:
                    next_generation_grid[i][j] = 1
        return next_generation_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if self.is_max_generations_exceeded:
            self.prev_generation = self.curr_generation
            self.curr_generation = self.get_next_generation()
            self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is not None:
            return self.generations <= self.max_generations
        return True

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as f:
            grid = [[int(col) for col in row.strip()] for row in f]
        game = GameOfLife((len(grid), len(grid[0])))
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as f:
            for row in self.curr_generation:
                for col in row:
                    f.write(str(col))
                f.write("\n")
