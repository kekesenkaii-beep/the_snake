from random import choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс каждого игрового объекта(змейка, яблоко)."""

    def __init__(self) -> None:
        self.position = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Метод отрисовки"""
        pass


class Apple(GameObject):
    """Дочерний класс, Базового "Игрового объекта" - Яблоко."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Метод, отвечает за рандомную позицию каждого "нового" яблока."""
        self.position = (
            choice(range(0, SCREEN_WIDTH, GRID_SIZE)),
            choice(range(0, SCREEN_HEIGHT, GRID_SIZE))
        )
        return self.position

    def draw(self):
        """
        Метод, отрисовывает класс "Яблоко",
        рисует квадрат по размерам игровой клетки (20х20 p.).
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self):
        """Метод рестарта игры, сброс позиции."""
        self.position = self.randomize_position()


class Snake(GameObject):
    """
    Дочерний класс, Базового "Игрового объекта" - Змейка,
    Дополненый аргументами: Длинна, Направление, Следующее направление.
    """

    def __init__(self):
        super().__init__()
        self.lenght = 23
        self.direction = LEFT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.positions = [self.position]

    def update_direction(self):
        """Метод обновления направления."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод расчета новой головы по заданному направлении."""
        head_x, head_y = self.positions[0]
        dx, dy = self.direction

        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)

        if len(self.positions) > self.lenght:
            self.positions.pop()

        self.position = new_head

    def get_head_position(self) -> tuple:
        """Обработка запроса, а где голова?"""
        return self.positions[0]

    def draw(self):
        """Метод отрисовки Змеи."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self):
        """Метод сброса игры до стартовых значений."""
        self.lenght = 1
        self.direction = LEFT
        self.next_direction = None
        self.positions = [self.position]


def handle_keys(game_object):
    """Метод обработки нажатий клавиатуры пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


# Главная функция, тут логика игры.
def main():
    """Главная функция игры, запуск игрового цикла, логика."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    # Основной цикл игры.
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()

        pygame.display.update()

        if apple.position == snake.position:
            snake.lenght += 1
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.reset()


if __name__ == '__main__':
    main()
