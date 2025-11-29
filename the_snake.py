from random import choice

import pygame as pg


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 540
GRID_UI = 60
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = (SCREEN_HEIGHT - GRID_UI) // GRID_SIZE
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = (SCREEN_HEIGHT - GRID_UI) // 2

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

UI_BACKGROUND_COLOR = (0, 0, 0)

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('"Змейка" Press ESC to Exit, Press SPACE to Speed Up')

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
        while True:
            new_position = (
                choice(range(0, SCREEN_WIDTH, GRID_SIZE)),
                choice(range(0, (SCREEN_HEIGHT - GRID_UI), GRID_SIZE))
            )
            if new_position not in forbidden:
                self.position = new_position
                return self.position


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
        self.current_speed = SPEED
        self.positions = [self.position]
        self.score = 0

    def update_direction(self) -> None:
        """Метод обновления направления."""
        if self.next_direction:
            if OPPOSITE_DIRECTIONS[self.direction] != self.next_direction:
                self.direction = self.next_direction

    def move(self):
        """Метод расчета новой головы по заданному направлении."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        self.position = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % (SCREEN_HEIGHT - GRID_UI)
        )
        self.positions.insert(0, self.position)
        if len(self.positions) > self.lenght:
            last = self.positions.pop()
            last_rect = pg.Rect(last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Метод сброса игры до стартовых значений."""
        self.lenght = 1
        self.score = 0
        self.positions.clear()
        self.position = (CENTER_X, CENTER_Y)
        self.positions.append(self.position)

    def get_head_position(self) -> tuple:
        """Обработка запроса, а где голова?"""
        return self.positions[0]


class UserInterface(GameObject):
    """
    Дочерний класс, Базового класа "Игровой объект" - UI
    Доп.аргументы: Очки.
    """

    body_color = UI_BACKGROUND_COLOR

    def __init__(self):
        super().__init__()
        self.position = (0, SCREEN_HEIGHT - GRID_UI)
        self.font = pg.font.Font(None, 36)

    def draw(self):
        """Отрисовка бэкграунда"""
        rect = pg.Rect(self.position, (SCREEN_WIDTH, GRID_UI))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def user_text(self, score: int):
        """Создание текста, описание кол-ва текущих очков."""
        return self.font.render(
            f'Очки: {score}',
            True,
            (180, 0, 0)
        )

    def record_text(self, record_score: int):
        """Создание текста, описание кол-ва рекордных очков."""
        return self.font.render(
            f'Рекорд: {record_score}',
            True,
            (180, 0, 0)
        )


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
    apple = Apple()
    snake = Snake()
    user_interface = UserInterface()
    backend = Backend()

    # Основной цикл игры.
    while True:
        handle_keys(snake)
        clock.tick(snake.current_speed)
        snake.update_direction()
        snake.move()

        if apple.position == snake.position:
            snake.lenght += 1
            snake.score += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[3:]:
            backend.save_score(snake.score)
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        user_interface.draw()
        record_score = backend.get_best_score()
        user_text_surf = user_interface.user_text(snake.score)
        record_text_surf = user_interface.record_text(record_score)

        screen.blit(user_text_surf, (20, SCREEN_HEIGHT - GRID_UI + 10))
        screen.blit(record_text_surf, (20, SCREEN_HEIGHT - GRID_UI + 35))
        pg.display.update()


if __name__ == '__main__':
    main()
