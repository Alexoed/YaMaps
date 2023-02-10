import pygame

from MapReturner import ImageGenerator


FPS = 60
interface = pygame.sprite.Group()


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
    delta = 20

    generator = ImageGenerator()
    picture = Picture(pygame.image.load(
        generator.get_from_toponym(toponym, str(delta / 100_000))[1]
    ))
    x, y = generator.get_position()
    redraw = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    delta = min(max(delta + 20, 20), 100_000)
                    redraw = True
                elif event.key == pygame.K_PAGEDOWN:
                    delta = min(max(delta - 20, 20), 100_000)
                    redraw = True
                elif event.key == pygame.K_r:
                    redraw = True
        if redraw:
            print("\rДельта:", delta, end="")
            picture.set_picture(pygame.image.load(
                generator.get_from_cords(x, y, str(delta / 100_000))[1]
            ))
            redraw = False
        screen.fill(pygame.Color("black"))
        interface.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
