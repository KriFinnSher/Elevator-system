# импортируем pygame
import pygame

# Константы
SCREEN_WIDTH = 470
SCREEN_HEIGHT = 770
FLOOR_COUNT = 11
FREIGHT_ELEVATOR_WIDTH = 75
ELEVATOR_WIDTH = 50
ELEVATOR_HEIGHT = 70
BUTTON_SIZE = 20
FLOOR_HEIGHT = 70
BLACK = (0, 0, 0)

# Инициализация Pygame
pygame.init()
# создаём объект для главного экрана
# с указанием ширины и высоты
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# указываем название для главного окна
pygame.display.set_caption("Два лифта")

# загружаем изображения
# картинка для лифта
elevator_img = pygame.image.load("elevator.jpg").convert_alpha()
# картинка для красной кнопки
button1_elevator1 = pygame.image.load("button1_elevator1.png").convert_alpha()
# картинка для синей кнопки
button1_elevator2 = pygame.image.load("button1_elevator2.png").convert_alpha()
# картинка для грузового лифта
freight_elevator_img = pygame.image.load("freight_elevator.jpg").convert_alpha()
# картинка для фона
back_img = pygame.image.load("back.jpg").convert_alpha()

# масштабируем изображения под заданные в константах размеры
elevator_img = pygame.transform.scale(elevator_img, (ELEVATOR_WIDTH, ELEVATOR_HEIGHT))
button1_elevator1 = pygame.transform.scale(button1_elevator1, (BUTTON_SIZE, BUTTON_SIZE))
button1_elevator2 = pygame.transform.scale(button1_elevator2, (BUTTON_SIZE, BUTTON_SIZE))
freight_elevator_img = pygame.transform.scale(freight_elevator_img, (FREIGHT_ELEVATOR_WIDTH, ELEVATOR_HEIGHT))
back_img = pygame.transform.scale(back_img, (SCREEN_WIDTH, SCREEN_HEIGHT))


# класс Кнопок вызова
class Button:
   # конструктор __init__ создаёт кнопку
   def __init__(self, x, y, image, action, enabled=True):
       # рисуем прямоугольник с заданными координатами
       self.rect = pygame.Rect(x, y, BUTTON_SIZE, BUTTON_SIZE)
       # в прямоугольник вписываем изображение
       self.image = image
       # привязываем кнопку к функции, которую укажем при создании кнопки
       self.action = action
       # свойство - нажата кнопка или нет
       self.is_active = False
       # свойство - отключена кнопка или нет
       self.enabled = enabled

   # метод для отрисовки кнопки на главном экране с заданными координатами
   def draw(self, screen_func):
       # если кнопка отключена:
       if not self.enabled:
           # создаём изображение и указываем через параметр
           # pygame.SRCALPHA, что у него будут уровни прозрачности
           disabled_image = pygame.Surface((BUTTON_SIZE, BUTTON_SIZE), pygame.SRCALPHA)
           # копируем исходное изображение кнопки
           disabled_image.blit(self.image, (0, 0))
           # накладываем на исходное изображение тёмный полупрозрачный серый цвет
           disabled_image.fill((50, 50, 50, 200), special_flags=pygame.BLEND_RGBA_MULT)
           # метод blit рисует новый объект на изображении screen_func
           screen_func.blit(disabled_image, (self.rect.x, self.rect.y))
       # если кнопка не нажата:
       elif not self.is_active:
           # создаём изображение и указываем через параметр
           # pygame.SRCALPHA, что у него будут уровни прозрачности
           inactive_image = pygame.Surface((BUTTON_SIZE, BUTTON_SIZE), pygame.SRCALPHA)
           # копируем исходное изображение кнопки
           inactive_image.blit(self.image, (0, 0))
           # накладываем на исходное изображение полупрозрачный серый цвет
           inactive_image.fill((100, 100, 100, 150), special_flags=pygame.BLEND_RGBA_MULT)
           # метод blit рисует новый объект на изображении screen_func
           screen_func.blit(inactive_image, (self.rect.x, self.rect.y))
       # если кнопка активна, рисуем оригинальное изображение без затемнения
       # это создаёт эффект "горящей" кнопки
       else:
           # метод blit рисует новый объект на изображении screen_func
           screen_func.blit(self.image, (self.rect.x, self.rect.y))

   # метод проверки нажатия кнопки
   def check_click(self, pos):
       # проверяем, активна ли кнопка, включена и нажал ли на неё пользователь
       if not self.is_active and self.enabled and self.rect.collidepoint(pos):
           # если пользователь кликнул на неактивную работающую
           # кнопку, включаем указанную при создании функцию
           self.action()
           # активируем кнопку после нажатия
           self.is_active = True

   # метод для управления состоянием кнопки - нажата или нет
   def set_active(self, state):
       # устанавливаем True или False
       self.is_active = state

   # метод для управления состоянием кнопки - работает или нет
   def set_enabled(self, state):
       # устанавливаем True или False
       self.enabled = state


# класс Этажей
# создаёт этаж с кнопками для вызова двух лифтов.
# их координаты зависят от номера этажа (y)
class Floor:
   # конструктор __init__ создаёт этаж
   def __init__(self, y, elevator1, elevator2):
       # передаём номер этажа
       self.y = y
       # передаём на каждый этаж по два объекта кнопок,
       # размещаем на нужных местах соответственно этажу
       # и привязываем к нужному лифту через лямбда-функцию
       self.buttons = [
           Button(110, y + FLOOR_HEIGHT // 2 - BUTTON_SIZE // 2, button1_elevator1, lambda: elevator1.set_target(y)),
           Button(335, y + FLOOR_HEIGHT // 2 - BUTTON_SIZE // 2, button1_elevator2, lambda: elevator2.set_target(y)),
       ]

   # метод отрисовки этажа и кнопки
   def draw(self, screen_func):
       # рисуем линию на главном экране с толщиной 1
       # от нулевой координаты до конца
       # экрана по оси х и на высоте этаже y
       pygame.draw.line(screen, BLACK, (0, self.y), (SCREEN_WIDTH, self.y), 1)
       # рисуем кнопки на каждом этаже
       for button in self.buttons:
           button.draw(screen_func)


# класс Лифта
class Elevator:
   # определяем лифт с координатами, размерами и изображением
   def __init__(self, x, y, width, height, image):
       # начальные координаты
       self.x = x
       self.y = y
       # размеры лифта
       self.width = width
       self.height = height
       # изображение
       self.image = image
       # добавляем очередь для нажатых кнопок
       self.queue = []
       # скорость лифта
       self.speed = 2

   # метод для установки этажа, куда должен ехать лифт
   def set_target(self, y):
       # если этаж уже не находится в списке, добавляем его туда
       if y not in self.queue:
           self.queue.append(y)

   # Метод для движения лифтов
   def move(self):
       # проверяем, есть ли в очереди этажи для передвижения
       if not self.queue:
           # если в очереди-списке нет этажей, то есть
           # нет нажатых кнопок, метод сразу завершается
           return

       # берём первый элемент в очереди, к которому должен ехать лифт
       target_y = self.queue[0]
       # если лифт ниже целевого этажа, едем вверх,
       # то есть увеличиваем координату y
       if self.y < target_y:
           self.y += self.speed
           if self.y > target_y:
               self.y = target_y
       # если лифт выше целевого этажа, едем вниз,
       # то есть уменьшаем координату y
       elif self.y > target_y:
           self.y -= self.speed
           if self.y < target_y:
               self.y = target_y

       # как только лифт достиг целевого этажа,
       # убираем элемент из списка командой .pop()
       if self.y == target_y:
           self.queue.pop(0)
           # проверяем кнопки...
           for floor in system.floors:
               # и деактивируем кнопку на текущем этаже
               if floor.y == target_y:
                   for button in floor.buttons:
                       button.set_active(False)

   # метод для отрисовки лифтов на главном экране
   def draw(self, screen_func):
       screen_func.blit(self.image, (self.x, self.y))


# класс для создания всей Системы Лифтов
class ElevatorSystem:
   def __init__(self):
       # cоздаём два лифта: грузовой и пассажирский
       self.elevator1 = Elevator(150, SCREEN_HEIGHT - FLOOR_HEIGHT,
                                 FREIGHT_ELEVATOR_WIDTH, ELEVATOR_HEIGHT, freight_elevator_img)
       self.elevator2 = Elevator(255, SCREEN_HEIGHT - FLOOR_HEIGHT,
                                 ELEVATOR_WIDTH, ELEVATOR_HEIGHT, elevator_img)
       # создаём массив этажей
       self.floors = [
           Floor(SCREEN_HEIGHT - FLOOR_HEIGHT * (i + 1), self.elevator1, self.elevator2)
           for i in range(FLOOR_COUNT)
       ]

   # Отключает кнопку для конкретного лифта на указанном этаже
   def disable_elevator_button(self, floor_index, elevator_index):
       # если выбранный этаж находится в пределах допустимного количества этажей...
       if 0 <= floor_index < len(self.floors) and 0 <= elevator_index < len(self.floors[floor_index].buttons):
           # включаем кнопку
           self.floors[floor_index].buttons[elevator_index].set_enabled(False)

   # Включает кнопку для конкретного лифта на указанном этаже
   def enable_elevator_button(self, floor_index, elevator_index):
       # если выбранный этаж находится в пределах допустимного количества этажей...
       if 0 <= floor_index < len(self.floors) and 0 <= elevator_index < len(self.floors[floor_index].buttons):
           # включаем кнопку
           self.floors[floor_index].buttons[elevator_index].set_enabled(True)

   # метод обновления положения лифтов, созданный в классе Elevator
   def update(self):
       self.elevator1.move()
       self.elevator2.move()

   # метод отрисовки объектов
   def draw(self, screen_func):
       # рисуем этажи через метод draw класса Floor
       for floor in self.floors:
           floor.draw(screen_func)
       # рисуем лифты через метод draw класса Elevator
       self.elevator1.draw(screen_func)
       self.elevator2.draw(screen_func)


# основная функция
def main():
   # объект частоты обновления экрана
   clock = pygame.time.Clock()
   # объявляем глобальную область видимости для переменной
   global system
   # создаём объект класса Системы Лифтов
   system = ElevatorSystem()
   # флаг-метка для работы главного цикла
   running = True

   # пока флаг-метка равен True, работает цикл всей системы
   while running:
       # отрисовываем фон
       screen.blit(back_img, (0, 0))

       # проверяем список событий при запущенной программе
       for event in pygame.event.get():
           # если пользователь закрыл главное окно...
           if event.type == pygame.QUIT:
               # завершаем цикл
               running = False
           # если пользователь кликнул мышкой...
           elif event.type == pygame.MOUSEBUTTONDOWN:
               # сохраняем координаты клика в переменную pos
               pos = pygame.mouse.get_pos()
               # проверяем все этажи и кнопки для проверки,
               # совпадают ли координаты клика с одной из кнопок
               for floor in system.floors:
                   for button in floor.buttons:
                       button.check_click(pos)

           # Пример отключения кнопки для пассажирского лифта на 3-м этаже
           elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_1:  # Клавиша "1" отключает пассажирский лифт на 3-м этаже
                   system.disable_elevator_button(2, 1)

               elif event.key == pygame.K_2:  # Клавиша "2" включает пассажирский лифт на 3-м этаже
                   system.enable_elevator_button(2, 1)

       # обновляет состояние лифтов
       system.update()
       # отрисовывает лифты на нужных позициях
       system.draw(screen)
       # обновляем изображение для пользователя, создавая анимацию
       pygame.display.flip()
       # устанавливаем скорость обновления кадров до 30 в секунду
       clock.tick(60)

   # завершаем работу после окончания цикла
   pygame.quit()


# запускаем главную функцию
main()