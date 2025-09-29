import pygame
import random

class Screamer:
    def __init__(self, ventana, ancho, alto):
        self.ventana = ventana
        self.ANCHO = ancho
        self.ALTO = alto
        
        self.imagenes = [pygame.image.load("assets/image.png")]
        self.imagenes = [pygame.transform.scale(img, (self.ANCHO, self.ALTO)) for img in self.imagenes]

        self.sonido_susto = pygame.mixer.Sound("assets/espanto.mp3")
        self.sonido_susto.set_volume(0.6)

        self.mostrando = False
        self.tiempo_inicio = 0
        self.duracion = 500  # ms
        self.proximo_screamer = pygame.time.get_ticks() + random.randint(10000, 20000)
        self.imagen_actual = None

    def actualizar(self):
        ahora = pygame.time.get_ticks()
        if not self.mostrando and ahora >= self.proximo_screamer:
            self.mostrando = True
            self.tiempo_inicio = ahora
            self.imagen_actual = random.choice(self.imagenes)
            self.sonido_susto.play()
        if self.mostrando and ahora - self.tiempo_inicio > self.duracion:
            self.mostrando = False
            self.proximo_screamer = ahora + random.randint(20000, 40000)

    def dibujar(self):
        if self.mostrando and self.imagen_actual:
            self.ventana.blit(self.imagen_actual, (0, 0))
            return True
        return False