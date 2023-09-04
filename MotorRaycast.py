import pygame
import math

pygame.init()

AnchoPantalla = 640
AlturaPantalla = 480

ventana = pygame.display.set_mode((AnchoPantalla, AlturaPantalla))
pygame.display.set_caption("Raycasting")

AnchoMapa = 16
AlturaMapa = 16

mapa = [
    "################",
    "#..............#",
    "#.......####...#",
    "#...#......#...#",
    "#...#......#...#",
    "#####......#...#",
    "#......##......#",
    "#...........##.#",
    "#...######.....#",
    "#..........##..#",
    "#...##.........#",
    "#......##......#",
    "#..............#",
    "#..##......##..#",
    "#......####....#",
    "################"
]
PosX = 2.0
PosY = 2.0

AnguloJugador = math.pi / 2.0
FOV = math.pi / 4.0
Profundidad = 20.0
Velocidad = 0.2
VelocidadRotacion = 0.12

reloj = pygame.time.Clock()

ColorFondo = (152, 255, 152)
ColorGrisOscuro = (40, 40, 40)

pantalla_titulo = True

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

    if pantalla_titulo:
        ventana.fill((90, 0, 90))

        titulo_font = pygame.font.Font(None, 36)
        titulo_texto = titulo_font.render("Motor Raycasting, prueba", True, (255, 255, 255))
        titulo_rect = titulo_texto.get_rect(center=(AnchoPantalla // 2, AlturaPantalla // 2 - 40))
        ventana.blit(titulo_texto, titulo_rect)

        instrucciones_font = pygame.font.Font(None, 24)
        instrucciones_texto = instrucciones_font.render("Presione espacio para continuar", True, (255, 255, 255))
        instrucciones_rect = instrucciones_texto.get_rect(center=(AnchoPantalla // 2, AlturaPantalla // 2 + 40))
        ventana.blit(instrucciones_texto, instrucciones_rect)

        pygame.display.flip()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_SPACE]:
            pantalla_titulo = False

    else:
        ventana.fill(ColorFondo)

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w]:
            PosX += math.cos(AnguloJugador) * Velocidad
            PosY += math.sin(AnguloJugador) * Velocidad
        if teclas[pygame.K_s]:
            PosX -= math.cos(AnguloJugador) * Velocidad
            PosY -= math.sin(AnguloJugador) * Velocidad
        if teclas[pygame.K_a]:
            AnguloJugador -= VelocidadRotacion
        if teclas[pygame.K_d]:
            AnguloJugador += VelocidadRotacion

        for i in range(AnchoPantalla):
            anguloRayo = (AnguloJugador - FOV / 2.0) + (i / AnchoPantalla) * FOV
            DistanciaPared = 0.0
            VecX = math.cos(anguloRayo)
            VecY = math.sin(anguloRayo)
            ColisionPared = False

            while not ColisionPared and DistanciaPared < Profundidad:
                RayoX = int(PosX + VecX * DistanciaPared)
                RayoY = int(PosY + VecY * DistanciaPared)

                if (
                    RayoX < 0
                    or RayoX >= AnchoMapa
                    or RayoY < 0
                    or RayoY >= AlturaMapa
                ):
                    DistanciaPared = Profundidad
                    ColisionPared = True
                elif mapa[RayoY][RayoX] == "#":
                    ColisionPared = True
                DistanciaPared += 0.1

            Pared = int((AlturaPantalla / 2.0) - AlturaPantalla / (2 * DistanciaPared))
            Suelo = AlturaPantalla - Pared

            for j in range(AlturaPantalla):
                if j <= Pared:
                    pygame.draw.rect(ventana, (0, 0, 0), (i, j, 1, 1))
                elif Pared < j < Suelo:
                    distancia_normalizada = min(1.0, DistanciaPared / Profundidad)
                    r = int(255 * (1 - distancia_normalizada))  # Cambio a blanco
                    g = int(255 * (1 - distancia_normalizada))  # Cambio a blanco
                    b = int(255 * (1 - distancia_normalizada))  # Cambio a blanco
                    pygame.draw.rect(ventana, (r, g, b), (i, j, 1, 1))
                else:
                    pygame.draw.rect(ventana, ColorGrisOscuro, (i, j, 1, 1))

        pygame.draw.rect(ventana, (255, 255, 102), (int(PosX) - 5, int(PosY) - 5, 10, 10))

        pygame.display.flip()
        reloj.tick(60)
