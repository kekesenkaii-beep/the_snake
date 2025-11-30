from random import choice

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
CENTER = (CENTER_X, CENTER_Y)
ALL_CELLS = {
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
}

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Словарь с обратными направлениями:
OPPOSITE_DIRECTIONS = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT
}

# Константы скорости:
SPEED = 20
FAST_SPEED = 30

BOARD_BACKGROUND_COLOR = (128, 128, 128)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс каждого игрового объекта(змейка, яблоко)."""

    def __init__(self) -> None:
        self.body_color = None
        self.position = CENTER

    def draw_cell(self, position, body_color):
        """Рисует одну ячейку нужным цветом."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)

    def draw(self):
        """Базовый метод отрисовки объекта (переопределяется в потомках)."""
        # Добавил для прохождения тестов
        self.draw_cell(self.position, self.body_color)


class Apple(GameObject):
    """Дочерний класс, Базового "Игрового объекта" - Яблоко."""

    def __init__(self, forbidden_cells=None, color=APPLE_COLOR):
        super().__init__()
        self.randomize_position(forbidden_cells)
        self.body_color = color

    def randomize_position(self, forbidden_cells=None):
        """Метод, отвечает за рандомную позицию каждого "нового" яблока."""
        if forbidden_cells is None:
            forbidden_cells = []

        forbidden_set = set(forbidden_cells)
        free_cells = ALL_CELLS - forbidden_set
        self.position = choice(tuple(free_cells))

    def draw(self):
        """Отрисовка Яблока"""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """
    Дочерний класс, Базового "Игрового объекта" - Змейка,
    Дополненый аргументами: Длинна, Направление, Следующее направление.
    """

    def __init__(self, color=SNAKE_COLOR):
        super().__init__()
        self.body_color = color
        self.reset()
        self.current_speed = SPEED

    def update_direction(self, next_direction):
        """Метод обновления направления."""
        if OPPOSITE_DIRECTIONS[self.direction] != next_direction:
            self.direction = next_direction

    def move(self):
        """Метод расчета новой головы по заданному направлении."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        self.position = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, self.position)

        if len(self.positions) > self.lenght:
            tail = self.positions.pop()
            self.draw_cell(tail, BOARD_BACKGROUND_COLOR)

    def reset(self):
        """Метод сброса игры до стартовых значений."""
        self.lenght = 1
        self.direction = LEFT
        self.positions = [CENTER]

    def get_head_position(self) -> tuple:
        """Обработка запроса, а где голова?"""
        return self.positions[0]

    def draw(self):
        """Отрисовка змейки"""
        for position in self.positions:
            self.draw_cell(position, self.body_color)


class Backend:
    """
    Отдельный класс Бэкэнда.
    Обработка файлов, возврат рекордного кол-ва очков.
    """

    def __init__(self):
        self.file_name = 'result.txt'

    def save_score(self, score: int) -> None:
        """СОбработка файла, записываем очки."""
        with open(self.file_name, 'a', encoding='utf-8') as file:
            file.write(f'{score}\n')

    def get_best_score(self) -> int:
        """Обработка файла, возвращаем рекорд."""
        best_score = 0
        with open(self.file_name, 'r', encoding='utf-8') as file:
            for line in file:
                score = int(line.strip())
                if score > best_score:
                    best_score = score
        return best_score


def handle_keys(snake):
    """Метод обработки нажатий клавиатуры пользователя."""
    for event in pg.event.get():
        is_quit = event.type == pg.QUIT
        is_escape = event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
        if is_quit or is_escape:
            pg.quit()
            raise SystemExit

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                snake.update_direction(UP)
            elif event.key == pg.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pg.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pg.K_RIGHT:
                snake.update_direction(RIGHT)

    pressed_keys = pg.key.get_pressed()
    snake.current_speed = FAST_SPEED if pressed_keys[pg.K_SPACE] else SPEED


# Главная функция, тут логика игры.
def main():
    """Главная функция игры, запуск игрового цикла, логика."""
    # Инициализация pg:
    pg.init()
    pg.font.init()
    # Тут нужно создать экземпляры классов.
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake = Snake()
    apple = Apple(snake.positions)
    backend = Backend()
    score = 1

    # Основной цикл игры.
    while True:
        handle_keys(snake)
        clock.tick(snake.current_speed)
        snake.move()

        if apple.position == snake.position:
            snake.lenght += 1
            score += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[3:]:
            backend.save_score(score)
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        record_score = backend.get_best_score()
        pg.display.set_caption(
            '"Змейка". "ESC" - выход "SPACE" - ускорение.'
            f'Очки: {score} Рекорд: {record_score}.'
        )
        pg.display.update()


if __name__ == '__main__':
    main()
