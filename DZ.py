import pygame
import random
import os

# Инициализация Pygame и звуковой системы
pygame.init()
pygame.mixer.init()  # Инициализация звуковой системы

# Настройки окна
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Survival Game")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Настройки игрока
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 80
PLAYER_SPEED = 5

# Настройки других автомобилей
CAR_WIDTH = 50
CAR_HEIGHT = 80
CAR_SPEED = 5
CAR_SPAWN_RATE = 50

# Загрузка изображений
try:
    player_image = pygame.image.load("player_car.png")  # Автомобиль игрока
    enemy_image = pygame.image.load("enemy_car.png")    # Автомобиль врага
except FileNotFoundError:
    print("Ошибка: Не удалось загрузить изображения. Убедитесь, что файлы player_car.png и enemy_car.png находятся в той же папке.")
    pygame.quit()
    exit()

# Масштабирование изображений
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
enemy_image = pygame.transform.scale(enemy_image, (CAR_WIDTH, CAR_HEIGHT))

# Загрузка музыки
try:
    pygame.mixer.music.load("sigma_bojj.mp3")  # Фоновая музыка
    pygame.mixer.music.set_volume(0.5)  # Установите громкость (от 0.0 до 1.0)
    pygame.mixer.music.play(-1)  # Воспроизведение музыки в цикле
    print("Музыка успешно загружена и воспроизводится.")
except pygame.error as e:
    print(f"Ошибка при загрузке музыки: {e}")
    print("Убедитесь, что файл sigma_bojj.mp3 находится в текущей рабочей директории.")

# Загрузка звуковых эффектов
try:
    crash_sound = pygame.mixer.Sound("crash_sound.wav")  # Звук столкновения
    crash_sound.set_volume(1.0)  # Установите громкость звука (от 0.0 до 1.0)
    print("Звук столкновения успешно загружен.")
except pygame.error as e:
    print(f"Ошибка при загрузке звука столкновения: {e}")
    print("Убедитесь, что файл crash_sound.wav находится в текущей рабочей директории.")
    crash_sound = None  # Если звук не загружен, установите его в None

# Класс игрока (автомобиль)
class Player:
    def __init__(self):
        self.x = WIDTH // 2 - PLAYER_WIDTH // 2
        self.y = HEIGHT - 100
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

    def move(self, dx):
        self.x += dx
        # Ограничение движения в пределах экрана
        self.x = max(0, min(self.x, WIDTH - self.width))

    def draw(self):
        WIN.blit(player_image, (self.x, self.y))

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
        WIN.blit(enemy_image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Функция для отображения текста "FINISH!!!!!"
def show_finish_screen():
    WIN.fill(BLACK)  # Черный фон
    font = pygame.font.SysFont(None, 100)  # Шрифт для текста
    text = font.render("FINISH!!!!!", True, WHITE)  # Текст "FINISH!!!!!"
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Центрирование текста
    WIN.blit(text, text_rect)  # Отображение текста
    pygame.display.update()  # Обновление экрана
    pygame.time.delay(3000)  # Задержка перед завершением (3 секунды)

# Основная функция игры
def main():
    clock = pygame.time.Clock()
    player = Player()
    cars = []
    running = True
    score = 0

    while running:
        clock.tick(60)
        WIN.fill(GREEN)  # Зеленый фон (трасса)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-PLAYER_SPEED)
        if keys[pygame.K_RIGHT]:
            player.move(PLAYER_SPEED)

        # Спавн других автомобилей
        if random.randint(1, CAR_SPAWN_RATE) == 1:
            cars.append(Car())

        # Движение и отрисовка других автомобилей
        for car in cars:
            car.move()
            car.draw()

            # Проверка столкновения
            if player.get_rect().colliderect(car.get_rect()):
                if crash_sound:  # Если звук загружен
                    crash_sound.play()  # Воспроизведение звука столкновения
                running = False  # Остановка игры
                show_finish_screen()  # Показать экран "FINISH!!!!!"
                break  # Выйти из цикла

        # Удаление автомобилей, которые уехали за экран
        cars = [car for car in cars if car.y < HEIGHT]

        # Отрисовка игрока
        player.draw()

        # Отображение счета
        score += 1
        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f"Score: {score}", True, BLACK)
        WIN.blit(score_text, (10, 10))

        pygame.display.update()

    pygame.quit()

# Запуск игры
if __name__ == "__main__":
    main()