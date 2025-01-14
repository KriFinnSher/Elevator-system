import pygame
import os

# global constants
WINDOW_W = 470
WINDOW_H = 770
FLOOR_COUNT = 11
ELEVATOR_W = 50
ELEVATOR_H = 70
FREIGHT_ELEVATOR_W = 75
BUTTON_SIZE = 20
FLOOR_H = 70
BLACK = (0, 0, 0)

# directory for images
media_dir = "media\\"

pygame.init() # initialize all imported pygame modules

# set width and height of main window + caption
main_window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption('СУЛ')

# add images of each object
elevator_img = pygame.image.load(os.path.join(media_dir, 'elevator.jpg'))
red_btn_img = pygame.image.load(os.path.join(media_dir, 'red_button.png')).convert_alpha()
blue_btn_img = pygame.image.load(os.path.join(media_dir, 'blue_button.png')).convert_alpha()
freight_elevator_img = pygame.image.load(os.path.join(media_dir, 'freight_elevator.jpg'))
background_img = pygame.image.load(os.path.join(media_dir, 'background.jpg'))

# scale size of each object
elevator_img = pygame.transform.scale(elevator_img, (ELEVATOR_W, ELEVATOR_H))
freight_elevator_img = pygame.transform.scale(freight_elevator_img, (FREIGHT_ELEVATOR_W, ELEVATOR_H))
red_btn_img = pygame.transform.scale(red_btn_img, (BUTTON_SIZE, BUTTON_SIZE))
blue_btn_img = pygame.transform.scale(blue_btn_img, (BUTTON_SIZE, BUTTON_SIZE))
background_img  = pygame.transform.scale(background_img, (WINDOW_W, WINDOW_H))


class Button:
    def __init__(self, x, y, image, action):
        self.rect = pygame.Rect(x, y, BUTTON_SIZE, BUTTON_SIZE)
        self.image = image
        self.action = action

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def was_clicked(self, position):
        if self.rect.collidepoint(position):
            self.action()


class Floor:
    def __init__(self, y, elevator_1, elevator_2):
        self.y = y
        self.buttons = [
            Button(110, y + FLOOR_H // 2 - BUTTON_SIZE // 2, red_btn_img,
                   lambda: elevator_1.set_target(y)),
            Button(335, y + FLOOR_H // 2 - BUTTON_SIZE // 2, blue_btn_img,
                   lambda: elevator_2.set_target(y))
        ]

    def draw(self, window):
        pygame.draw.line(window, BLACK, (0, self.y), (WINDOW_W, self.y), 1)

        for button in self.buttons:
            button.draw(window)


class Elevator:
    def __init__(self, x, y, w_, h_, image):
        self.x = x
        self.y = y
        self.width = w_
        self.height = h_
        self.image = image
        self.target_y = y
        self.speed = 2

    def move(self):
        if self.y > self.target_y:
            self.y -= self.speed
        elif self.y < self.target_y:
            self.y += self.speed

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def set_target(self, y):
        self.target_y = y
        pass


class ElevatorSystem:
    def __init__(self):
        self.freight_elevator = Elevator(150, WINDOW_H - FLOOR_H, FREIGHT_ELEVATOR_W, ELEVATOR_H, freight_elevator_img)
        self.elevator = Elevator(255, WINDOW_H - FLOOR_H, ELEVATOR_W, ELEVATOR_H, elevator_img)

        self.floors = [
            Floor(WINDOW_H - (i + 1) * FLOOR_H, self.freight_elevator, self.elevator)
            for i in range(FLOOR_COUNT)
        ]

    def draw(self, window):
        for floor in self.floors:
            floor.draw(window)
        self.freight_elevator.draw(window)
        self.elevator.draw(window)

    def update(self):
        self.freight_elevator.move()
        self.elevator.move()



def main():
   clock = pygame.time.Clock()
   running = True
   system = ElevatorSystem()

   while running:
       main_window.blit(background_img, (0, 0))

       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False
           elif event.type == pygame.MOUSEBUTTONDOWN:
               pos = pygame.mouse.get_pos()
               for floor in system.floors:
                   for button in floor.buttons:
                       button.was_clicked(pos)

       system.update()
       system.draw(main_window)
       pygame.display.flip()
       clock.tick(60)

   pygame.quit()

main()