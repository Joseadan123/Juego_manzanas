import pygame
import sys
from config import BLANCO, FUENTE


def mostrar_menu(ventana, texto, opciones, fuente, color):
    ventana.fill((0, 0, 0))
    titulo = fuente.render(texto, True, color)
    ventana.blit(titulo, (ventana.get_width() // 2 - titulo.get_width() // 2, 200))

    botones = []
    for i, opcion in enumerate(opciones):
        txt = fuente.render(opcion, True, color)
        rect = txt.get_rect(center=(ventana.get_width() // 2, 350 + i * 60))
        ventana.blit(txt, rect)
        botones.append((opcion, rect))
    pygame.display.flip()
    return botones


def menu_inicio(juego):
    while True:
        botones = mostrar_menu(juego.ventana, "Recolecta las Manzanas", ["Jugar", "Salir"], FUENTE, BLANCO)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for opcion, rect in botones:
                    if rect.collidepoint(evento.pos):
                        if opcion == "Jugar":
                            return
                        elif opcion == "Salir":
                            pygame.quit()
                            sys.exit()


def menu_final(juego, resultado):
    while True:
        texto = "¡Ganaste!" if resultado == "ganaste" else "¡Perdiste!"
        botones = mostrar_menu(juego.ventana, texto, ["Volver a jugar", "Salir"], FUENTE, BLANCO)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for opcion, rect in botones:
                    if rect.collidepoint(evento.pos):
                        if opcion == "Volver a jugar":
                            juego.resetear()
                            return
                        elif opcion == "Salir":
                            pygame.quit()
                            sys.exit()
