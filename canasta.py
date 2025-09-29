import pygame

class Canasta:
    def __init__(self, imagen, ancho, alto):
        self.image = imagen
        self.ancho = ancho   # guardar dimensiones reales
        self.alto = alto
        self.rect = self.image.get_rect()
        self.rect.midbottom = (ancho // 2, alto)  # posición inicial: abajo centrado
        self.vel = 10  # velocidad

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.vel
        if teclas[pygame.K_RIGHT] and self.rect.right < self.ancho:  # usar ancho real
            self.rect.x += self.vel

    def dibujar(self, ventana):
        ventana.blit(self.image, self.rect)