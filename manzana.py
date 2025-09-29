import pygame
import random

class Manzana:
    def __init__(self, img_roja, img_verde, pos_x, pos_y):
        self.tipo = random.choice(["roja"] * 4 + ["verde"])
        self.image = img_roja if self.tipo == "roja" else img_verde
        self.rect = self.image.get_rect(midtop=(pos_x, pos_y))
        self.vel = random.randint(2, 5)

    def mover(self):
        self.rect.y += self.vel

    def dibujar(self, ventana):
        ventana.blit(self.image, self.rect)
