import pygame
import os
from MapReturner import ImageGenerator


pygame.init()
screen_size = width, height = 600, 450
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

FPS = 60
interface = pygame.sprite.Group()
SCALE = 100_000
HALF_SCALE = SCALE / 2


def inside(x, y, rect):
    """Проверяет вхождение точки в прямоугольную область"""
    return (rect.x <= x <= rect.x + rect.w and
            rect.y <= y <= rect.y + rect.h)


def load_image(name, colorkey=None):
    """Загружает указанное изображение, если может.
    Вырезает фон."""
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        raise Exception(f"Файл с изображением '{fullname}' не найден")
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def mirror(image):
    """Отражает изображение по вертикали (вдоль оси x)"""
    return pygame.transform.flip(image, True, False)


def cut_sheet(sheet, columns, rows, mirror_line=-1):
    """Режет изображение на его составляющие"""
    frames = []
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                       sheet.get_height() // rows)
    for j in range(rows):
        temp = []
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            temp.append(sheet.subsurface(pygame.Rect(
                frame_location, rect.size)))
        frames.append(temp)
        if j == mirror_line - 1:
            frames.append([mirror(image) for image in temp])
    return frames


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


class Button(pygame.sprite.Sprite):
    """Кнопка интерфейса"""
    images = cut_sheet(load_image("button.png", -1), 2, 2)

    def __init__(self, position, text, groups=interface):
        """Инициализация кнопки, отрисовка текста на ней."""
        super().__init__(groups)
        self.state = self.images[0]
        self.image = self.state[0].copy()
        self.rect = self.image.get_rect()
        self.shift = 2
        # инициализация шрифта
        font = pygame.font.SysFont("ComicSans", 28 - len(text))
        self.string_text = text
        self.text = font.render(text, True, (255, 255, 255))

        self.rect.x, self.rect.y = position

    def hold(self, pos):
        """Нажимает на кнопку. Возвращает истину,
        если нажата успешно."""
        if inside(*pos, self.rect):
            self.state = self.images[1]
            self.shift = 0
            return True
        return False

    def release(self, pos):
        """Отпускает кнопку. Возвращает истину,
        если нажатие завершено верно."""
        if inside(*pos, self.rect):
            self.state = self.images[0]
            # если эта кнопка была нажата
            if self.shift == 0:
                self.shift = 2
                return True
        else:
            self.state = self.images[0]
        self.shift = 2
        return False

    def get_text(self):
        """Возвращает свой текст"""
        return self.string_text

    def update(self, pos):
        """Обновление состояния"""
        # если наведён курсор, то выделится
        if inside(*pos, self.rect):
            self.image = self.state[1].copy()
        else:
            self.image = self.state[0].copy()
        self.image.blit(self.text, (
            (self.rect.w - self.text.get_width()) // 2 - self.shift,
            (self.rect.h - self.text.get_height()) // 2 - self.shift
        ))


def text_object(string, pos_x=0, pos_y=0, size=40, color=(0, 0, 0)):
    """Создаёт и возвращает надпись"""
    font = pygame.font.SysFont("ComicSans", size)
    string_rendered = font.render(string, True, color)
    text_position = string_rendered.get_rect()
    text_position.x = pos_x
    text_position.y = pos_y
    return string_rendered, text_position


def main():
    global screen_size, width, height, screen, clock
    half_width = width // 2
    half_height = height // 2
    font = pygame.font.Font(None, 14)
    source_toponym = "Кириши, Ленинградская 6"
    toponym = source_toponym
    delta = 25

    generator = ImageGenerator()
    picture = Picture(pygame.image.load(
        generator.get_from_toponym(toponym, str(delta / SCALE))[1]
    ))
    g_x, g_y = map(float, generator.get_position())
    x, y = g_x, g_y
    movement_delta = HALF_SCALE
    mov_slow = False
    pressed_button = None
    redraw = False
    running = True
    write_postalcode = False
    # print(f"\rДельта: {delta}; Медленнее: {mov_slow}", end="")
    buttons = [
        Button((width - 200, height - 50), "вид"),
        Button((width - 200, height - 100), "сброс"),
        Button((width - 200, height - 150), "почтовый код")
    ]
    found_address = text_object(generator.get_address(), size=12)

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
                        generator.get_from_toponym(
                            toponym, str(delta / SCALE))
                        x, y = generator.get_position()
                        found_address = text_object(
                            generator.get_address(), size=12
                        )
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                ui_button_pressed = False
                for button in buttons:
                    if button.hold(event.pos):
                        ui_button_pressed = True
                        break
                if event.button == 1 and not ui_button_pressed:
                    # считаем долю смещения
                    x, y = event.pos
                    width_fraction = (x - half_width) / half_width
                    height_fraction = (half_height - y) / half_height
                    # добавляем долю от дельты
                    x, y = map(float, generator.get_position())
                    g_x += delta / SCALE * width_fraction
                    g_y += delta / SCALE * height_fraction
                    # picture.set_picture(pygame.image.load(
                    #     generator.get_from_cords(
                    #         str(g_x), str(g_y), str(delta / SCALE)
                    #     )[1]
                    # ))
                    generator.get_from_toponym(
                        str(g_x) + str(g_y), delta / SCALE)

            if event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    if button.release(event.pos):
                        if button.get_text() == "вид":
                            redraw = True
                            try:
                                layers = ('map', 'sat', 'sat,skl')
                                generator.set_layer(layers[layers.index(
                                    generator.layer) + 1])
                            except IndexError:
                                generator.set_layer('map')
                        elif button.get_text() == "сброс":
                            toponym = source_toponym
                            generator.get_from_toponym(
                                toponym, str(delta / SCALE))
                            x, y = generator.get_position()
                            found_address = text_object(
                                generator.get_address(), size=12
                            )
                            redraw = True
                        elif button.get_text() == "почтовый код":
                            write_postalcode = not write_postalcode
                            generator.set_postalcode(write_postalcode)
                            generator.get_from_toponym(
                                toponym, str(delta / SCALE))
                            x, y = generator.get_position()
                            found_address = text_object(
                                generator.get_address(), size=12
                            )
                            redraw = True

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
        interface.update(pygame.mouse.get_pos())
        interface.draw(screen)
        txt_surface = font.render(toponym, True, color)
        input_box.w = max(200, txt_surface.get_width() + 10)
        # Blit the text.
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)
        # Blit text
        screen.blit(*found_address)

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
