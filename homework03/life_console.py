import curses
import curses.ascii
from curses import KEY_MOUSE

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.clear()

        height, width = screen.getmaxyx()
        line = ""
        height, width = screen.getmaxyx()
        line = ""
        for row in range(height):
            for col in range(width):
                if row != height - 1 and row != 0:
                    if row > 0 and (row + 1) > height:
                        if col == 0 or col == width - 1:
                            line += "|"
                        else:
                            line += " "
                else:
                    if col == 0 or col == width - 1:
                        line += "+"
                    else:
                        line += "-"

            try:
                screen.addstr(line)
            except curses.error:
                pass
            line = ""

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """

        height, width = screen.getmaxyx()
        shift_y = (height - self.life.rows) // 2
        shift_x = (width - self.life.cols) // 2

        for i, row in enumerate(self.life.curr_generation):
            for j, col in enumerate(row):
                if col:
                    try:
                        screen.addstr(i + shift_y, j + shift_x, "*")
                    except curses.error:
                        pass
        screen.refresh()
        screen.getch()

    def run(self) -> None:
        screen = curses.initscr()

        max_row, max_col = screen.getmaxyx()
        if self.life.rows >= max_row:
            mesg = "Строк слишком много. Уменьшите их количество."
            screen.addstr(max_row // 2, (max_col - len(mesg)) // 2, mesg)
            screen.getch()
        elif self.life.cols >= max_col:
            mesg = "Столбцов слишком много. Уменьшите их количество."
            screen.addstr(max_row // 2, (max_col - len(mesg)) // 2, mesg)
            screen.getch()
        else:

            screen.keypad(True)
            curses.noecho()
            screen.nodelay(True)

            key = -1
            while self.life.is_changing and self.life.is_max_generations_exceeded:
                if key == curses.ascii.ESC:
                    break
                self.draw_borders(screen)
                self.draw_grid(screen)
                self.life.step()

                prev_key = key
                event = screen.getch()
                key = key if event == -1 else event

                if key == curses.ascii.SP:
                    key = -1
                    while key != curses.ascii.SP:
                        key = screen.getch()
                    key = prev_key
                    continue
                if key != curses.ascii.ESC:
                    key = prev_key

        screen.keypad(False)
        curses.echo()
        curses.endwin()


if __name__ == "__main__":
    gof = GameOfLife((24, 75))
    game = Console(gof)
    game.run()
