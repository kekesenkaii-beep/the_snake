from random import choice
import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2

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

BOARD_BACKGROUND_COLOR = (128, 128, 128)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('"Змейка" Press ESC to Exit')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс каждого игрового объекта(змейка, яблоко)."""

    body_color = tuple[int, int, int]

    def __init__(self) -> None:
        self.position = (CENTER_X, CENTER_Y)

    def draw(self):
        """Метод отрисовки"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Дочерний класс, Базового "Игрового объекта" - Яблоко."""

    body_color = APPLE_COLOR

    def __init__(self):
        super().__init__()
        self.randomize_position([])

    def randomize_position(self, forbidden):
        """Метод, отвечает за рандомную позицию каждого "нового" яблока."""
        new_posistion = (
            choice(range(0, SCREEN_WIDTH, GRID_SIZE)),
            choice(range(0, SCREEN_HEIGHT, GRID_SIZE))
        )
        if new_posistion not in forbidden:
            self.position = new_posistion


class Snake(GameObject):
    """
    Дочерний класс, Базового "Игрового объекта" - Змейка,
    Дополненый аргументами: Длинна, Направление, Следующее направление.
    """

    body_color = SNAKE_COLOR

    def __init__(self):
        super().__init__()
        self.lenght = 1
        self.direction = LEFT
        self.next_direction = None
        self.positions = [self.position]

    def update_direction(self) -> None:
        """Метод обновления направления."""
        if self.next_direction:
            if OPPOSITE_DIRECTIONS[self.direction] != self.next_direction:
                self.direction = self.next_direction

    def reset(self):
        """Метод сброса игры до стартовых значений."""
        del self.positions[1:]
        self.lenght = 1
        self.direction = LEFT

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
            last = self.positions.pop()
            last_rect = pg.Rect(last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple:
        """Обработка запроса, а где голова?"""
        return self.positions[0]


def handle_keys(snake):
    """Метод обработки нажатий клавиатуры пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            if event.key == pg.K_UP:
                snake.next_direction = UP
            elif event.key == pg.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pg.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pg.K_RIGHT:
                snake.next_direction = RIGHT


# Главная функция, тут логика игры.
def main():
    """Главная функция игры, запуск игрового цикла, логика."""
    # Инициализация pg:
    pg.init()
    # Тут нужно создать экземпляры классов.
    screen.fill(BOARD_BACKGROUND_COLOR)
    apple = Apple()
    snake = Snake()

    # Основной цикл игры.
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if apple.position == snake.position:
            snake.lenght += 1
            apple.randomize_position(snake.positions)
        if snake.get_head_position() in snake.positions[3:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
