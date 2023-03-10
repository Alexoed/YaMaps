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
    font = pygame.font.Font(None, 14)
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    toponym = "Кириши, Ленинградская 6"
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
    # print(f"\rДельта: {delta}; Медленнее: {mov_slow}", end="")

    input_box = pygame.Rect(10, 410, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        generator.get_from_toponym(toponym, str(delta / SCALE))
                        x, y = generator.get_position()
                        redraw = True
                    elif event.key == pygame.K_BACKSPACE:
                        toponym = toponym[:-1]
                    else:
                        toponym += event.unicode
                elif event.key == pygame.K_PAGEUP:
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
                elif event.key == pygame.K_SLASH:
                    redraw = True
                    try:
                        layers = ('map', 'sat', 'sat,skl')
                        generator.set_layer(layers[layers.index(
                            generator.layer) + 1])
                    except IndexError:
                        generator.set_layer('map')

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
        txt_surface = font.render(toponym, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
