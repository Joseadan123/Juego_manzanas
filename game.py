import pygame
import sys
import random
from config import BLANCO, FUENTE
from canasta import Canasta
from manzana import Manzana
from screamer import Screamer

class Juego:
    def __init__(self):
        self.ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Recolecta las manzanas")

        # Dimensiones
        self.ANCHO, self.ALTO = self.ventana.get_size()
        self.reloj = pygame.time.Clock()

        # Fondo
        self.fondo = pygame.image.load("assets/fondo.png")
        self.fondo = pygame.transform.scale(self.fondo, (self.ANCHO, self.ALTO))

        # Canasta
        canasta_img = pygame.image.load("assets/canasta.png")
        canasta_img = pygame.transform.scale(canasta_img, (120, 120))  
        self.canasta = Canasta(canasta_img, self.ANCHO, self.ALTO)

        # Manzanas
        self.img_roja = pygame.image.load("assets/manzana_roja.png")
        self.img_roja = pygame.transform.scale(self.img_roja, (60, 60))
        self.img_verde = pygame.image.load("assets/manzana_verde.png")
        self.img_verde = pygame.transform.scale(self.img_verde, (60, 60))

        # Musica de fondo
        pygame.mixer.init()
        pygame.mixer.music.load("assets/musica_fondo.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        # Sonido de manzana roja
        self.sonido_roja = pygame.mixer.Sound("assets/sonido_manzana.mp3")
        self.sonido_verde = pygame.mixer.Sound("assets/sonido_verde.mp3")

        # Abarca toda la pantalla el screamer 
        self.screamer = Screamer(self.ventana, self.ANCHO, self.ALTO)

        # Estado inicial
        self.resetear()

        # Posiciones en el árbol
        centro_x = self.ANCHO // 2
        base_y = 160
        separacion_x = 200
        self.posicion_arbol = [
            (centro_x - separacion_x, base_y + 30),
            (centro_x, base_y),
            (centro_x + separacion_x, base_y + 40),
            (centro_x - separacion_x // 2, base_y + 80),
            (centro_x + separacion_x // 2, base_y + 70),
        ]

    def resetear(self):
        self.manzanas = []
        self.puntos_rojos = 0
        self.verdes_cogidas = 0
        self.rojas_caidas = 0

    def generar_manzana(self):
        max_manzanas = 4    
        if len(self.manzanas) < max_manzanas:
            if random.random() < 0.10:
                pos = random.choice(self.posicion_arbol)
                manzana = Manzana(self.img_roja, self.img_verde, pos[0], pos[1])
                manzana.tiempo_en_arbol = pygame.time.get_ticks()
                manzana.en_arbol = True
                manzana.rect.y = pos[1]
                self.manzanas.append(manzana)

        tiempo_espera = 800
        ahora = pygame.time.get_ticks()
        for m in self.manzanas:
            if getattr(m, "en_arbol", False):
                if ahora - m.tiempo_en_arbol >= tiempo_espera:
                    m.en_arbol = False
                else:
                    m.rect.y = getattr(m, "tiempo_en_arbol_pos", m.rect.y)
                    m.tiempo_en_arbol_pos = m.rect.y

    def verificar_colisiones(self):
        self.canasta_hitbox = self.canasta.rect.copy()
        self.canasta_hitbox.x += 20
        self.canasta_hitbox.width -= 40
        self.canasta_hitbox.y += 70
        self.canasta_hitbox.height = 10

        for m in self.manzanas[:]:
            if m.rect.top > self.ALTO:
                if m.tipo == "roja":
                    self.rojas_caidas += 1
                self.manzanas.remove(m)
            elif m.rect.colliderect(self.canasta_hitbox):
                if m.tipo == "roja":
                    self.puntos_rojos += 1
                    self.sonido_roja.play()
                else:
                    self.verdes_cogidas += 1
                    self.sonido_verde.play()
                self.manzanas.remove(m)

    def verificar_estado(self):
        if self.puntos_rojos >= 50:
            return "ganaste"
        if self.verdes_cogidas >= 3:
            return "perdiste_verdes"
        if self.rojas_caidas >= 3:
            return "perdiste_rojas"
        return None

    def dibujar(self):
        self.ventana.blit(self.fondo, (0, 0))
        self.canasta.dibujar(self.ventana)
        pygame.draw.rect(self.ventana, (255, 0, 0), self.canasta_hitbox, 2)  # rojo, borde de 2 px

        for m in self.manzanas:
            m.dibujar(self.ventana)

        marcador = FUENTE.render(
            f"Rojas: {self.puntos_rojos} | Verdes: {self.verdes_cogidas} | Caidas: {self.rojas_caidas}",
            True, BLANCO
        )
        self.ventana.blit(marcador, (20, 20))
        pygame.display.flip()

    def bucle_principal(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Actualizar juego normal
            teclas = pygame.key.get_pressed()
            self.canasta.mover(teclas)
            self.generar_manzana()
            for m in self.manzanas:
                m.mover()
            self.verificar_colisiones()
            estado = self.verificar_estado()
            if estado:
                return estado

            # Actualizar y dibujar screamer
            self.screamer.actualizar()  
            self.dibujar()               
            self.screamer.dibujar()      
            pygame.display.flip()        

            self.reloj.tick(60)