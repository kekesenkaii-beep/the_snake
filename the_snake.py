from random import choice

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
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

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс каждого игрового объекта(змейка, яблоко)."""

    def __init__(self, color=None) -> None:
        self.body_color = color
        self.position = CENTER

    def draw_cell(self, position, color, with_border=True):
        """Базовая зарисовка ячейки, с флагом наличия "Рамки"."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        if with_border:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Базовый метод отрисовки объекта (переопределяется в потомках)."""
        # Добавил для прохождения тестов
        pass


class Apple(GameObject):
    """Дочерний класс, Базового "Игрового объекта" - Яблоко."""

    # Поменял значение по умолчанию forbidden_cells,
    # на создание пустого кортежа. Pytest не проходит.
    def __init__(self, forbidden_cells=()):
        super().__init__(color=APPLE_COLOR)
        self.randomize_position(forbidden_cells)

    def randomize_position(self, forbidden_cells=()):
        """Метод, отвечает за рандомную позицию каждого "нового" яблока."""
        free_cells = ALL_CELLS - set(forbidden_cells)
        self.position = choice(tuple(free_cells))

    def draw(self):
        """Отрисовка Яблока"""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """
    Дочерний класс, Базового "Игрового объекта" - Змейка,
    Дополненый аргументами: Длинна, Направление, Следующее направление.
    """

    def __init__(self):
        super().__init__(color=SNAKE_COLOR)
        self.current_speed = SPEED
        self.reset()

    def draw(self):
        """Отрисовка змейки"""
        self.draw_cell(self.position, self.body_color)
        if self.last is not None:
            self.draw_cell(
                self.last,
                BOARD_BACKGROUND_COLOR,
                with_border=False
            )

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
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Метод сброса игры до стартовых значений."""
        self.lenght = 1
        self.direction = LEFT
        self.positions = [CENTER]
        self.last = None

    def get_head_position(self) -> tuple:
        """Обработка запроса, а где голова?"""
        return self.positions[0]


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
        if (
            event.type == pg.QUIT
            or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)
        ):
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

    pressed = pg.key.get_pressed()
    return pressed[pg.K_SPACE]


# Главная функция, тут логика игры.
def main():
    """Главная функция игры, запуск игрового цикла, логика."""
    # Инициализация pg:
    pg.init()
    # Тут нужно создать экземпляры классов.
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake = Snake()
    apple = Apple(snake.positions)
    backend = Backend()
    score = 1
    speed = SPEED

    # Основной цикл игры.
    while True:
        fast = handle_keys(snake)
        speed = FAST_SPEED if fast else SPEED
        clock.tick(speed)
        snake.move()
        apple.draw()
        snake.draw()

        if apple.position == snake.position:
            snake.lenght += 1
            score += 1
            apple.randomize_position(snake.positions)

        elif snake.get_head_position() in snake.positions[3:]:
            backend.save_score(score)
            snake.reset()
            score = 1
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

        record_score = backend.get_best_score()
        pg.display.set_caption(
            '"Змейка". "ESC" - выход "SPACE" - ускорение.'
            f'Очки: {score} Рекорд: {record_score}.'
        )
        pg.display.update()


if __name__ == '__main__':
    main()
