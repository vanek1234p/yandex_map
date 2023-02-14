import sys
import requests
import pygame
import os


spn1, spn2 = map(str, input().split())
coords1, coords2 = map(str, input().split())

maps_server = 'http://static-maps.yandex.ru/1.x/'
map_params = {
    'll': coords1 + ',' + coords2,
    'spn': spn1 + ',' + spn2,
    'l': 'map'}
response = requests.get(maps_server, params=map_params)
with open('data\\map.png', 'wb') as f:
    f.write(response.content)
image = pygame.image.load('data\\map.png')
os.remove('data\\map.png')
pygame.init()
pygame.display.set_caption('YL-MAP')
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
running = True
now = 0
FPS = 50
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def


while running:
    screen.blit(image, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()