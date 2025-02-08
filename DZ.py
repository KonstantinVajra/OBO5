import pygame
import random
import os

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Гонка")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 255, 0)

# Настройки игрока
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 80
PLAYER_SPEED = 5
PLAYER_BOOST = 4  # Ускорение в 4 раза
PLAYER_REVERSE = 0.5  # Замедление при движении назад

# Настройки других автомобилей
CAR_WIDTH = 50
CAR_HEIGHT = 80
CAR_SPEED = 5
CAR_SPAWN_RATE = 50

# Загрузка изображений
try:
    player_image = pygame.image.load("player_car.png")
    enemy_image = pygame.image.load("enemy_car.png")
    begin_image = pygame.image.load("begin.jpg")
    final_image = pygame.image.load("FINAL.jpg")
except FileNotFoundError as e:
    print(f"Ошибка загрузки изображений: {e}")
    pygame.quit()
    exit()

# Масштабирование изображений под размер экрана
begin_image = pygame.transform.scale(begin_image, (WIDTH, HEIGHT))
final_image = pygame.transform.scale(final_image, (WIDTH, HEIGHT))

player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
enemy_image = pygame.transform.scale(enemy_image, (CAR_WIDTH, CAR_HEIGHT))

# Функция загрузки звуков с проверкой
def load_sound(filename, volume=1.0, loop=False):
    if os.path.exists(filename):
        sound = pygame.mixer.Sound(filename)
        sound.set_volume(volume)
        if loop:
            sound.play(-1)  # Запуск в цикле
        return sound
    else:
        print(f"⚠ Внимание: Файл '{filename}' не найден. Звук отключён.")
        return None

# Звуки
crash_sound = load_sound("crash_sound.wav", volume=1.0)  # Звук аварии
motor_sound = load_sound("motor.wav", volume=0.5, loop=True)  # Звук мотора (в цикле)

# Фоновая музыка
if os.path.exists("sigma_bojj.mp3"):
    pygame.mixer.music.load("sigma_bojj.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)  # Запуск в цикле
else:
    print("⚠ Внимание: Файл 'sigma_bojj.mp3' не найден. Музыка отключена.")

# Функция начального экрана
def start_screen():
    font = pygame.font.SysFont(None, 80)
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 80)  # Координаты кнопки "СТАРТ"

    while True:
        screen.blit(begin_image, (0, 0))  # Отображение заставки

        pygame.draw.rect(screen, RED, button_rect)  # Рисуем кнопку
        text = font.render("СТАРТ", True, WHITE)
        screen.blit(text, (button_rect.x + 30, button_rect.y + 15))  # Текст на кнопке

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):  # Если нажали кнопку "СТАРТ"
                    return  # Начинаем игру

# Функция отображения экрана столкновения
def crash_screen():
    screen.blit(final_image, (0, 0))  # Отображаем картинку "FINAL.jpg"
    font = pygame.font.SysFont(None, 80)
    text = font.render("Ты не СИГМА!", True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 40))  # Отображение текста
    pygame.display.update()

    if crash_sound:
        crash_sound.play()

    pygame.mixer.music.stop()  # Остановка фоновой музыки
    if motor_sound:
        motor_sound.stop()  # Остановка звука мотора

    pygame.time.delay(3000)  # Задержка 3 секунды перед выходом
    pygame.quit()
    exit()

# Класс игрока
class Player:
    def __init__(self):
        self.x = WIDTH // 2 - PLAYER_WIDTH // 2
        self.y = HEIGHT - 100
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED

    def move(self, dx, dy):
        """Двигает машину влево/вправо и вперёд/назад."""
        self.x = max(0, min(self.x + dx * self.speed, WIDTH - self.width))
        self.y = max(0, min(self.y + dy * self.speed, HEIGHT - self.height))

    def draw(self):
        screen.blit(player_image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Класс других автомобилей
class Car:
    def __init__(self):
        self.x = random.randint(0, WIDTH - CAR_WIDTH)
        self.y = -CAR_HEIGHT
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.speed = CAR_SPEED

    def move(self):
        self.y += self.speed

    def draw(self):
        screen.blit(enemy_image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Основная функция игры
def main():
    start_screen()  # Показываем начальный экран с кнопкой "СТАРТ"

    clock = pygame.time.Clock()
    player = Player()
    cars = []
    running = True

    while running:
        clock.tick(60)
        screen.fill(GREEN)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Управление игроком
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -PLAYER_BOOST  # Ускорение вперёд
        if keys[pygame.K_DOWN]:
            dy = PLAYER_REVERSE  # Замедленный ход назад

        player.move(dx, dy)

        # Спавн машин
        if random.randint(1, CAR_SPAWN_RATE) == 1:
            cars.append(Car())

        # Движение машин и проверка столкновений
        for car in cars:
            car.move()
            car.draw()
            if player.get_rect().colliderect(car.get_rect()):
                crash_screen()  # Показываем экран столкновения

        # Удаление машин, которые уехали за экран
        cars = [car for car in cars if car.y < HEIGHT]

        # Отрисовка игрока
        player.draw()

        pygame.display.update()

    pygame.quit()

# Запуск игры
if __name__ == "__main__":
    main()
