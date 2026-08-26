"""Игра Змейка."""

from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 7

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


def handle_keys(self, event):
    """Обрабатывает нажатия клавиш."""
    if event.key == pygame.K_UP and self.direction != DOWN:
        self.next_direction = UP
    elif event.key == pygame.K_DOWN and self.direction != UP:
        self.next_direction = DOWN
    elif event.key == pygame.K_LEFT and self.direction != RIGHT:
        self.next_direction = LEFT
    elif event.key == pygame.K_RIGHT and self.direction != LEFT:
        self.next_direction = RIGHT


class GameObject:
    """Родительский класс, содержит общие атрибуты игровых объектов."""

    def __init__(
        self, body_color=(0, 255, 0),
        position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ):
        """Инициализирует игровой объект."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки объекта."""
        pass


class Apple(GameObject):
    """Отвечает за позицию яблока."""

    def __init__(self, position=(240, 200)):
        """Инициализирует яблоко."""
        super().__init__((255, 0, 0), position)

    def randomize_position(self):
        """Метод отвечает за случайную позицию яблока."""
        self.x = randint(0, 31) * GRID_SIZE
        self.y = randint(0, 23) * GRID_SIZE
        self.position = (self.x, self.y)

    def draw(self):
        """Отрисока яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Отвечает за движение змейки."""

    def __init__(
        self, positions=None, direction=RIGHT,
        next_direction=None, length=1, last=None
    ):
        """Инициализирует змейку."""
        if positions is None:
            positions = [
                (
                    randint(0, SCREEN_WIDTH - 1) * GRID_SIZE,
                    randint(0, SCREEN_HEIGHT - 1) * GRID_SIZE,
                )
            ]
        super().__init__((0, 255, 0), positions[0])
        self.length = length
        self.positions = positions
        self.direction = direction
        self.next_direction = next_direction
        self.last = last

    def get_head_position(self):
        """Метод получения позиции головы."""
        return self.positions[0]

    def move(self):
        """Метод, отвечающий за передвижение змейки."""
        current_head = self.get_head_position()
        head_position_x = current_head[0] + self.direction[0]
        head_position_y = current_head[1] + self.direction[1]
        new_head_position = (
            head_position_x % SCREEN_WIDTH,
            head_position_y % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head_position)

        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            del self.positions[-1]

    def update_direction(self):
        """Метод обновления направления движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Отрисовка змейки."""
        for position in self.positions[1:]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Метод возвращающий змейку в игру."""
        return Snake()


def main():
    """Запускает основной игровой цикл."""
    pygame.init()
    apple = Apple()
    apple.randomize_position()
    snake = Snake()

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        clock.tick(SPEED)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                handle_keys(snake, event)

        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            apple.randomize_position()
            snake.length += 1
        if snake.get_head_position() in snake.positions[1:]:
            apple = Apple()
            apple.randomize_position()
            snake = snake.reset()
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
