"""Импорт библиотек."""
import sys
from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
START_POSITION: tuple[int, int] = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

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
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class ExitGame(Exception):
    """Конец игры."""

    pass


class GameObject:
    """Базовый объект для создания остальных."""

    def __init__(self, body_color=None):
        """Цвет и позиция."""
        self.body_color = body_color
        self.position = START_POSITION

    def draw(self):
        """Заготовка для метода отрисовки."""
        pass


class Apple(GameObject):
    """Яблоко."""

    def __init__(self, body_color=APPLE_COLOR):
        """Передача цвета и случайная позиция."""
        super().__init__(body_color)
        self.randomize_position(positions=[START_POSITION])

    def draw(self):
        """Отрисовка класса Яблоко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, positions=None):
        """Рандомизация позиции."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )
        while self.position in positions:
            self.randomize_position(positions)


class Snake(GameObject):
    """Змейка."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Цвет, позиция, направления, длина."""
        super().__init__(body_color)
        self.reset()
        self.next_direction = None

    def draw(self):
        """Отрисовка класса Змейка."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Смена направления."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы."""
        return self.positions[0]

    def move(self):
        """Передвижение по координатам."""
        x_point, y_point = self.get_head_position()

        x_direction, y_direction = {
            RIGHT: (GRID_SIZE, 0),
            LEFT: (GRID_SIZE * -1, 0),
            UP: (0, GRID_SIZE * -1),
            DOWN: (0, GRID_SIZE)
        }[self.direction]

        new_x = (x_point + x_direction) % SCREEN_WIDTH
        new_y = (y_point + y_direction) % SCREEN_HEIGHT

        self.positions.insert(0, (new_x, new_y))
        self.last = self.positions.pop()

    def reset(self):
        """Сброс в центр экрана."""
        self.positions = [START_POSITION]
        self.length = 1
        self.direction = RIGHT
        self.last = None


def handle_keys(game_object):
    """Контроль ввода с клавиатуры."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise ExitGame
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Запуск игры."""
    pygame.init()
    apple = Apple(body_color=APPLE_COLOR)
    snake = Snake(body_color=SNAKE_COLOR)

    while True:
        clock.tick(SPEED)
        snake.update_direction()
        snake.move()

        try:
            handle_keys(snake)

        except ExitGame:
            pygame.quit()
            sys.exit()

        snake_head = snake.get_head_position()
        if snake_head == apple.position:
            snake.length += 1
            snake.positions.insert(0, apple.position)
            apple.randomize_position(snake.positions)

        elif snake_head in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
