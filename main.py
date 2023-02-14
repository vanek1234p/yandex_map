import sys
import requests
import pygame
import os


all_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = pygame.Color('black')
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Map(pygame.sprite.Sprite):
    def __init__(self, spn1, spn2, coords1, coords2):
        super().__init__(all_sprites)
        self.spn = [spn1, spn2]
        self.coords = [coords1, coords2]
        self.scale = 1.0
        self.size = 450, 450
        self.image = load_image("map.png")
        self.update_image()
        self.rect = self.image.get_rect()
        self.rect.top = 20
        self.rect.left = 20

    def update_image(self, coords: tuple=None, scale=None):
        if coords:
            self.coords = coords
        if scale:
            self.scale = scale
        maps_server = 'http://static-maps.yandex.ru/1.x/'
        map_params = {
            'll': ','.join([str(elem) for elem in self.coords]),
            'spn': ','.join([str(elem) for elem in self.spn]),
            'l': 'map',
            'scale': str(self.scale),
            'size': ','.join([str(elem) for elem in self.size])
        }
        response = requests.get(maps_server, params=map_params)
        with open('data\\map.png', 'wb') as f:
            f.write(response.content)
        self.image = load_image("map.png")


running = True
pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
map = Map(*map(float, '0.01 0.01 37.23452345 55.234562345'.split()))
dct_keys = {1073741899: 0.1, 1073741902: -0.1}
dct_keys_2 = {pygame.K_UP: (0, 1), pygame.K_DOWN: (0, -1), pygame.K_RIGHT: (2, 0), pygame.K_LEFT: (-2, 0)}


def terminate():
    pygame.quit()
    sys.exit()


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_PAGEUP and 1 <= map.scale + 0.1 <= 4:
                map.update_image(scale=map.scale + 0.1)
            if event.key == pygame.K_PAGEDOWN and 1 <= map.scale - 0.1 <= 4:
                map.update_image(scale=map.scale - 0.1)
            if event.key in dct_keys_2.keys():
                tup = dct_keys_2[event.key]
                new_coord = map.coords[0] + map.spn[0] * tup[0], map.coords[1] + map.spn[1] * tup[1]
                map.update_image(coords=new_coord)

    pygame.display.flip()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()