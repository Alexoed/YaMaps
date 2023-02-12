import pygame

from MapReturner import ImageGenerator


FPS = 60
interface = pygame.sprite.Group()
SCALE = 100_000
HALF_SCALE = SCALE / 2


class Picture(pygame.sprite.Sprite):
    """Позволяет установить и нарисовать картинку."""
    def __init__(self, image, groups=interface):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect()

    def set_position(self, x, y):
        """Переместить картинку"""
        self.rect = self.rect.move(x, y)

    def set_picture(self, image):
        """Сменить картинку"""
        self.image = image


def main():
    pygame.init()
    screen_size = width, height = 600, 450
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    toponym = "Кириши, ленинградская 6"
    delta = 25

    generator = ImageGenerator()
    picture = Picture(pygame.image.load(
        generator.get_from_toponym(toponym, str(delta / SCALE))[1]
    ))
    x, y = generator.get_position()
    movement_delta = HALF_SCALE
    mov_slow = False
    pressed_button = None
    redraw = False
    running = True
    print(f"\rДельта: {delta}; Медленнее: {mov_slow}", end="")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    delta = min(max(delta * 2, 12.5), 6_553_600)
                    redraw = True
                elif event.key == pygame.K_PAGEDOWN:
                    delta = min(max(delta / 2, 12.5), 6_553_600)
                    redraw = True
                elif event.key == pygame.K_RIGHT:
                    x = float(x) + delta / movement_delta
                    if x >= 180:
                        x = delta / movement_delta
                    x = str(x)
                    redraw = True
                elif event.key == pygame.K_LEFT:
                    x = float(x) - delta / movement_delta
                    if x <= 0:
                        x = 180 - delta / movement_delta
                    x = str(x)
                    redraw = True
                elif event.key == pygame.K_UP:
                    y = str(float(y) + delta / movement_delta)
                    pressed_button = 'up'
                    redraw = True
                elif event.key == pygame.K_DOWN:
                    y = str(float(y) - delta / movement_delta)
                    pressed_button = 'down'
                    redraw = True
                elif event.key == pygame.K_r:
                    redraw = True
                elif event.key == pygame.K_f:
                    mov_slow = not mov_slow
                    if mov_slow:
                        movement_delta = SCALE
                    else:
                        movement_delta = HALF_SCALE
                    print(f"\rДельта: {delta}; Медленнее: {mov_slow}",
                          end="")
        if redraw:
            print(f"\rДельта: {delta}; Медленнее: {mov_slow}",
                  end="")
            try:
                picture.set_picture(pygame.image.load(
                    generator.get_from_cords(x, y,
                                             str(delta / SCALE))[1]))
            except pygame.error:
                if pressed_button == 'up':
                    y = str(float(y) - delta / movement_delta)
                else:
                    y = str(float(y) + delta / movement_delta)
                picture.set_picture(pygame.image.load(
                    generator.get_from_cords(x, y,
                                             str(delta / SCALE))[1]))
            redraw = False
        screen.fill(pygame.Color("black"))
        interface.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
