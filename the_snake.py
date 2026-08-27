"""Игра Змейка."""

from random import randint
from typing import Tuple
import pygame as pg

# Алиасы для аннотации
Pointer = Tuple[int, int]
Color = Tuple[int, int, int]


# Константы для размеров поля и сетки:
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP: Pointer = (0, -GRID_SIZE)
DOWN: Pointer = (0, GRID_SIZE)
LEFT: Pointer = (-GRID_SIZE, 0)
RIGHT: Pointer = (GRID_SIZE, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: Color = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR: Color = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: Color = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR: Color = (0, 255, 0)

# Скорость движения змейки:
SPEED: int = 7

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


def handle_keys(snake: Snake) -> None:
    """Обрабатывает все игровые события."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


class GameObject:
    """Родительский класс, содержит общие атрибуты игровых объектов."""

    def __init__(
        self, body_color: Color = SNAKE_COLOR,
        position: Pointer = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ) -> None:
        """Инициализирует игровой объект."""
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """Метод отрисовки объекта."""
        raise NotImplementedError(
            "Метод draw() должен быть переопределён в дочернем классе"
        )


class Apple(GameObject):
    """Отвечает за позицию яблока."""

    def __init__(
            self, body_color: Color = APPLE_COLOR,
            position: Pointer = (240, 200)
    ):
        """Инициализирует яблоко."""
        super().__init__(body_color, position)

    def randomize_position(self) -> None:
        """Метод отвечает за случайную позицию яблока."""
        self.x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        self.y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (self.x, self.y)

    def draw(self) -> None:
        """Отрисовка яблока."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Отвечает за движение змейки."""

    def __init__(self, body_color: Color = SNAKE_COLOR) -> None:
        """Инициализирует змейку."""
        start_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        start_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        start_position = (start_x, start_y)
        super().__init__(body_color, start_position)
        self.length = 1
        self.positions = [start_position]
        self.direction = RIGHT
        self.next_direction: Pointer | None = None
        self.last: Pointer | None = None

    def get_head_position(self) -> Pointer:
        """Метод получения позиции головы."""
        return self.positions[0]

    def move(self) -> None:
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
            self.last = self.positions.pop()

    def update_direction(self) -> None:
        """Метод обновления направления движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self) -> None:
        """Отрисовка змейки."""
        for position in self.positions[1:]:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self) -> None:
        """Метод возвращающий змейку в игру."""
        start_x: int = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        start_y: int = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        start_position: Pointer = (start_x, start_y)
        self.length = 1
        self.positions = [start_position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.position = start_position


def main() -> None:
    """Запускает основной игровой цикл."""
    pg.init()
    apple = Apple()
    apple.randomize_position()
    snake = Snake()

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            apple.randomize_position()
            snake.length += 1
        if snake.get_head_position() in snake.positions[1:]:
            apple = Apple()
            apple.randomize_position()
            snake.reset()
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
