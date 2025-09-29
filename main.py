import pygame
from game import Juego
from menu import menu_inicio, menu_final

if __name__ == "__main__":
    pygame.init()
    juego = Juego()

    while True:
        menu_inicio(juego)  # Solo se muestra una vez al iniciar

        while True:  # Bucle de juego + reinicios
            resultado = juego.bucle_principal()
            accion = menu_final(juego, resultado)

            if accion == "reiniciar":
                continue  # Reinicia el juego sin pasar por el menú de inicio
            elif accion == "salir":
                pygame.quit()
                exit()
