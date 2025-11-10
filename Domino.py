import pygame
import random
import sys
import math
from enum import Enum

# Inicialización de Pygame
pygame.init()
pygame.mixer.init()

# Configuración de pantalla
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dominó de Lujo - Juego Premium")

# PALETA DE COLORES PREMIUM
COLORES = {
    "ORO_PRINCIPAL": (212, 175, 55),
    "ORO_SECUNDARIO": (245, 200, 80),
    "ORO_CLARO": (255, 215, 0),
    "ORO_OSCURO": (180, 150, 40),
    "NEGRO_LUJO": (10, 10, 10),
    "NEGRO_SUAVE": (20, 20, 20),
    "NEGRO_CARTA": (5, 5, 5),
    "PLATA": (192, 192, 192),
    "PLATA_OSCURO": (150, 150, 150),
    "BLANCO_PREMIUM": (245, 245, 245),
    "ROJO_LUJO": (180, 40, 40),
    "VERDE_LUJO": (40, 140, 40),
    "AZUL_LUJO": (30, 100, 180),
    "MORADO_LUJO": (120, 60, 180),
    "TRANSPARENTE": (0, 0, 0, 0)
}

# Estados del juego
class EstadoJuego(Enum):
    MENU = 0
    SELECCION_JUGADORES = 1
    REPARTIENDO = 2
    JUGANDO = 3
    FINALIZADO = 4
    PAUSA = 5

# Efectos de partículas
particulas = []

class Particula:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.uniform(2, 6)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = random.uniform(30, 60)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1
        self.life -= 1
        return self.life > 0
    
    def draw(self, surface):
        alpha = min(255, int(self.life * 4))
        color_with_alpha = (*self.color, alpha)
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, color_with_alpha, (int(self.size), int(self.size)), int(self.size))
        surface.blit(surf, (int(self.x - self.size), int(self.y - self.size)))

def crear_particulas(x, y, color, cantidad=15):
    for _ in range(cantidad):
        particulas.append(Particula(x, y, color))

# Clase Ficha de Dominó Premium
class Ficha:
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha
        self.ancho = 80
        self.alto = 160
        self.x = 0
        self.y = 0
        self.seleccionada = False
        self.rotada = False
        self.jugable = False
        self.color_puntos = COLORES["ORO_CLARO"]
        
        # Colores base premium para las fichas según su valor
        self.colores_base = [
            COLORES["BLANCO_PREMIUM"],  # 0
            (255, 220, 220),  # 1 - Rosa suave
            (255, 235, 200),  # 2 - Durazno
            (255, 255, 200),  # 3 - Amarillo claro
            (220, 255, 220),  # 4 - Verde claro
            (220, 230, 255),  # 5 - Azul claro
            (235, 220, 255),  # 6 - Lila claro
        ]
    
    def dibujar(self, x, y, rotada=False, escala=1.0):
        self.x = x
        self.y = y
        self.rotada = rotada
        
        # Aplicar escala
        ancho = int(self.ancho * escala) if not rotada else int(self.alto * escala)
        alto = int(self.alto * escala) if not rotada else int(self.ancho * escala)
        
        # Color de fondo según estado
        if self.seleccionada:
            color_fondo = COLORES["ORO_CLARO"]
        elif self.jugable:
            color_fondo = (200, 230, 255)  # Azul muy claro para jugables
        else:
            color_fondo = self.colores_base[max(self.izquierda, self.derecha)]
        
        # Dibujar sombra elegante
        pygame.draw.rect(screen, COLORES["NEGRO_SUAVE"], (x+4, y+4, ancho, alto), border_radius=10)
        
        # Dibujar fondo de la ficha con efecto premium
        self._dibujar_ficha_premium(x, y, ancho, alto, color_fondo)
        
        # Dibujar borde dorado
        grosor_borde = 3 if self.jugable else 2
        color_borde = COLORES["ORO_PRINCIPAL"] if self.jugable else COLORES["ORO_OSCURO"]
        pygame.draw.rect(screen, color_borde, (x, y, ancho, alto), grosor_borde, border_radius=10)
        
        # Dibujar línea divisoria con efecto dorado
        if not rotada:
            pygame.draw.line(screen, COLORES["ORO_SECUNDARIO"], 
                           (x + ancho // 2, y + 5), (x + ancho // 2, y + alto - 5), 3)
        else:
            pygame.draw.line(screen, COLORES["ORO_SECUNDARIO"], 
                           (x + 5, y + alto // 2), (x + ancho - 5, y + alto // 2), 3)
        
        # Dibujar puntos con efectos premium
        self._dibujar_puntos_premium(x, y, ancho, alto, rotada)
    
    def _dibujar_ficha_premium(self, x, y, ancho, alto, color_base):
        # Crear superficie para efectos premium
        surf = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        
        # Fondo principal con gradiente sutil
        for i in range(ancho):
            factor = i / ancho
            r = max(0, min(255, color_base[0] - int(20 * factor)))
            g = max(0, min(255, color_base[1] - int(20 * factor)))
            b = max(0, min(255, color_base[2] - int(20 * factor)))
            pygame.draw.line(surf, (r, g, b), (i, 0), (i, alto))
        
        # Efecto de brillo en la parte superior
        for i in range(alto // 3):
            alpha = 100 - (i * 100) // (alto // 3)
            color_brillo = (*COLORES["BLANCO_PREMIUM"], alpha)
            pygame.draw.line(surf, color_brillo, (0, i), (ancho, i))
        
        screen.blit(surf, (x, y))
    
    def _dibujar_puntos_premium(self, x, y, ancho, alto, rotada):
        radio = 8
        espacio = 15
        
        if not rotada:
            # Mitad izquierda
            centro_x_izq = x + ancho // 4
            centro_y_izq = y + alto // 2
            self._dibujar_puntos_valor_premium(centro_x_izq, centro_y_izq, self.izquierda, espacio, radio)
            
            # Mitad derecha
            centro_x_der = x + 3 * ancho // 4
            centro_y_der = y + alto // 2
            self._dibujar_puntos_valor_premium(centro_x_der, centro_y_der, self.derecha, espacio, radio)
        else:
            # Mitad superior
            centro_x_sup = x + ancho // 2
            centro_y_sup = y + alto // 4
            self._dibujar_puntos_valor_premium(centro_x_sup, centro_y_sup, self.izquierda, espacio, radio)
            
            # Mitad inferior
            centro_x_inf = x + ancho // 2
            centro_y_inf = y + 3 * alto // 4
            self._dibujar_puntos_valor_premium(centro_x_inf, centro_y_inf, self.derecha, espacio, radio)
    
    def _dibujar_puntos_valor_premium(self, centro_x, centro_y, valor, espacio, radio):
        # Patrones de puntos para cada valor (0-6) con disposición de dominó real
        patrones = {
            0: [],
            1: [(0, 0)],
            2: [(-1, -1), (1, 1)],
            3: [(-1, -1), (0, 0), (1, 1)],
            4: [(-1, -1), (-1, 1), (1, -1), (1, 1)],
            5: [(-1, -1), (-1, 1), (0, 0), (1, -1), (1, 1)],
            6: [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1)]
        }
        
        # Dibujar puntos con efecto premium
        for dx, dy in patrones[valor]:
            punto_x = centro_x + dx * espacio
            punto_y = centro_y + dy * espacio
            
            # Sombra del punto
            pygame.draw.circle(screen, COLORES["NEGRO_SUAVE"], (int(punto_x)+2, int(punto_y)+2), radio+1)
            
            # Punto principal dorado
            pygame.draw.circle(screen, COLORES["ORO_PRINCIPAL"], (int(punto_x), int(punto_y)), radio)
            
            # Brillo interior
            pygame.draw.circle(screen, COLORES["ORO_CLARO"], (int(punto_x)-2, int(punto_y)-2), radio//2)
    
    def get_rect(self):
        if self.rotada:
            return pygame.Rect(self.x, self.y, self.alto, self.ancho)
        else:
            return pygame.Rect(self.x, self.y, self.ancho, self.alto)
    
    def __str__(self):
        return f"[{self.izquierda}|{self.derecha}]"
    
    def es_doble(self):
        return self.izquierda == self.derecha
    
    def valor_total(self):
        return self.izquierda + self.derecha

# Clase Jugador Premium
class Jugador:
    def __init__(self, nombre, es_humano=True, dificultad="normal"):
        self.nombre = nombre
        self.fichas = []
        self.es_humano = es_humano
        self.dificultad = dificultad
        self.puntos = 0
        self.avatar_color = random.choice([
            COLORES["ORO_PRINCIPAL"],
            COLORES["ROJO_LUJO"], 
            COLORES["VERDE_LUJO"],
            COLORES["AZUL_LUJO"],
            COLORES["MORADO_LUJO"]
        ])
    
    def agregar_ficha(self, ficha):
        self.fichas.append(ficha)
    
    def remover_ficha(self, ficha):
        if ficha in self.fichas:
            self.fichas.remove(ficha)
            crear_particulas(ficha.x + ficha.ancho//2, ficha.y + ficha.alto//2, self.avatar_color, 10)
            return True
        return False
    
    def tiene_fichas(self):
        return len(self.fichas) > 0
    
    def contar_puntos(self):
        return sum(ficha.valor_total() for ficha in self.fichas)
    
    def buscar_fichas_jugables(self, extremo_izquierdo, extremo_derecho):
        jugables = []
        for ficha in self.fichas:
            if (ficha.izquierda == extremo_izquierdo or ficha.derecha == extremo_izquierdo or
                ficha.izquierda == extremo_derecho or ficha.derecha == extremo_derecho):
                ficha.jugable = True
                jugables.append(ficha)
            else:
                ficha.jugable = False
        return jugables
    
    def dibujar_avatar(self, x, y, es_turno_actual=False):
        # Dibujar círculo del avatar premium
        radio = 25
        color_borde = COLORES["ORO_CLARO"] if es_turno_actual else COLORES["PLATA"]
        grosor_borde = 4 if es_turno_actual else 2
        
        # Sombra del avatar
        pygame.draw.circle(screen, COLORES["NEGRO_SUAVE"], (x+2, y+2), radio+1)
        
        # Círculo principal
        pygame.draw.circle(screen, self.avatar_color, (x, y), radio)
        pygame.draw.circle(screen, color_borde, (x, y), radio, grosor_borde)
        
        # Icono según tipo de jugador
        if self.es_humano:
            # Icono de corona para humanos
            puntos_corona = [
                (x, y-8),
                (x-5, y-3),
                (x-3, y-3),
                (x-3, y+2),
                (x+3, y+2),
                (x+3, y-3),
                (x+5, y-3)
            ]
            pygame.draw.polygon(screen, COLORES["ORO_CLARO"], puntos_corona)
        else:
            # Icono de engranaje para CPU
            pygame.draw.circle(screen, COLORES["PLATA"], (x, y), 8, 2)
            for angulo in range(0, 360, 45):
                rad = math.radians(angulo)
                px = x + math.cos(rad) * 12
                py = y + math.sin(rad) * 12
                pygame.draw.line(screen, COLORES["PLATA"], (x, y), (px, py), 2)

# Clase Mesa Premium
class Mesa:
    def __init__(self):
        self.fichas = []
        self.extremo_izquierdo = None
        self.extremo_derecho = None
        self.animacion_fichas = []
    
    def colocar_ficha_inicial(self, ficha):
        self.fichas = [ficha]
        self.extremo_izquierdo = ficha.izquierda
        self.extremo_derecho = ficha.derecha
        self.animacion_fichas.append({"ficha": ficha, "progreso": 0, "destino_x": WIDTH//2, "destino_y": HEIGHT//2})
    
    def colocar_ficha_izquierda(self, ficha):
        if ficha.derecha == self.extremo_izquierdo:
            self.fichas.insert(0, ficha)
            self.extremo_izquierdo = ficha.izquierda
        elif ficha.izquierda == self.extremo_izquierdo:
            ficha.rotada = not ficha.rotada
            ficha.izquierda, ficha.derecha = ficha.derecha, ficha.izquierda
            self.fichas.insert(0, ficha)
            self.extremo_izquierdo = ficha.izquierda
        
        # Animación - posicionar en el lado izquierdo (vertical)
        destino_x = 100  # margen izquierdo
        destino_y = HEIGHT//2 - (len([f for f in self.fichas if f.rotada]) * ficha.ancho) // 2
        self.animacion_fichas.append({"ficha": ficha, "progreso": 0, "destino_x": destino_x, "destino_y": destino_y})
        return True
    
    def colocar_ficha_derecha(self, ficha):
        if ficha.izquierda == self.extremo_derecho:
            self.fichas.append(ficha)
            self.extremo_derecho = ficha.derecha
        elif ficha.derecha == self.extremo_derecho:
            ficha.rotada = not ficha.rotada
            ficha.izquierda, ficha.derecha = ficha.derecha, ficha.izquierda
            self.fichas.append(ficha)
            self.extremo_derecho = ficha.derecha
        
        # Animación - posicionar en el lado derecho (vertical)
        destino_x = WIDTH - 100 - ficha.alto  # margen derecho
        destino_y = HEIGHT//2 - (len([f for f in self.fichas if f.rotada]) * ficha.ancho) // 2
        self.animacion_fichas.append({"ficha": ficha, "progreso": 0, "destino_x": destino_x, "destino_y": destino_y})
        return True
    
    def actualizar_animaciones(self):
        for anim in self.animacion_fichas[:]:
            anim["progreso"] += 0.1
            if anim["progreso"] >= 1:
                self.animacion_fichas.remove(anim)
    
    def dibujar(self):
        # Dibujar fondo de mesa premium (terciopelo negro)
        screen.fill(COLORES["NEGRO_LUJO"])
        
        # Patrón de textura sutil
        for i in range(0, WIDTH, 60):
            for j in range(0, HEIGHT, 60):
                alpha = 5 + ((i + j) // 60) % 2 * 5
                color_textura = (COLORES["NEGRO_SUAVE"][0], COLORES["NEGRO_SUAVE"][1], COLORES["NEGRO_SUAVE"][2], alpha)
                surf_textura = pygame.Surface((60, 60), pygame.SRCALPHA)
                pygame.draw.rect(surf_textura, color_textura, (0, 0, 60, 60))
                screen.blit(surf_textura, (i, j))
        
        # Borde decorativo dorado
        pygame.draw.rect(screen, COLORES["ORO_PRINCIPAL"], (0, 0, WIDTH, HEIGHT), 15, border_radius=8)
        pygame.draw.rect(screen, COLORES["ORO_OSCURO"], (7, 7, WIDTH-14, HEIGHT-14), 8, border_radius=5)
        pygame.draw.rect(screen, COLORES["NEGRO_LUJO"], (12, 12, WIDTH-24, HEIGHT-24), 4, border_radius=3)
        
        # Dibujar fichas en la mesa con animaciones
        if not self.fichas:
            return
        
        # Dibujar fichas animadas
        for anim in self.animacion_fichas:
            ficha = anim["ficha"]
            progreso = anim["progreso"]
            
            # Calcular posición interpolada
            if progreso < 1:
                start_x = WIDTH // 2
                start_y = HEIGHT // 2
                current_x = start_x + (anim["destino_x"] - start_x) * progreso
                current_y = start_y + (anim["destino_y"] - start_y) * progreso
                escala = 0.5 + 0.5 * progreso
            else:
                current_x = anim["destino_x"]
                current_y = anim["destino_y"]
                escala = 1.0
            
            ficha.dibujar(current_x - ficha.ancho//2, current_y - ficha.alto//2, ficha.rotada, escala)
        
        # Dibujar fichas estáticas - NUEVA DISTRIBUCIÓN SIMILAR A LA IMAGEN
        if len(self.fichas) <= 8:
            # Para pocas fichas, distribución lineal simple
            for i, ficha in enumerate(self.fichas):
                x = WIDTH//2 - (len(self.fichas) * ficha.ancho)//2 + i * ficha.ancho
                y = HEIGHT//2 - ficha.alto//2
                ficha.dibujar(x, y, False)
        else:
            # Para muchas fichas, distribución en forma de U como en la imagen
            total_fichas = len(self.fichas)
            
            # Calcular cuántas fichas irán en cada lado
            # En la imagen: superior (horizontal), derecha (vertical), inferior (horizontal), izquierda (vertical)
            fichas_por_lado = total_fichas // 4
            sobrante = total_fichas % 4
            
            # Asignar fichas a cada lado
            lados = {
                "superior": fichas_por_lado + (1 if sobrante > 0 else 0),
                "derecha": fichas_por_lado + (1 if sobrante > 1 else 0),
                "inferior": fichas_por_lado + (1 if sobrante > 2 else 0),
                "izquierda": fichas_por_lado
            }
            
            # Margen desde el borde
            margen = 100
            espacio_entre_fichas = 5
            
            indice_ficha = 0
            
            # LADO SUPERIOR (horizontal)
            for i in range(lados["superior"]):
                if indice_ficha >= total_fichas:
                    break
                ficha = self.fichas[indice_ficha]
                ficha.rotada = False
                ancho_total = lados["superior"] * ficha.ancho + (lados["superior"] - 1) * espacio_entre_fichas
                x = WIDTH//2 - ancho_total//2 + i * (ficha.ancho + espacio_entre_fichas)
                y = margen
                ficha.dibujar(x, y, False)
                indice_ficha += 1
            
            # LADO DERECHO (vertical)
            for i in range(lados["derecha"]):
                if indice_ficha >= total_fichas:
                    break
                ficha = self.fichas[indice_ficha]
                ficha.rotada = True
                alto_total = lados["derecha"] * ficha.ancho + (lados["derecha"] - 1) * espacio_entre_fichas
                x = WIDTH - margen - ficha.alto
                y = HEIGHT//2 - alto_total//2 + i * (ficha.ancho + espacio_entre_fichas)
                ficha.dibujar(x, y, True)
                indice_ficha += 1
            
            # LADO INFERIOR (horizontal)
            for i in range(lados["inferior"]):
                if indice_ficha >= total_fichas:
                    break
                ficha = self.fichas[indice_ficha]
                ficha.rotada = False
                ancho_total = lados["inferior"] * ficha.ancho + (lados["inferior"] - 1) * espacio_entre_fichas
                x = WIDTH//2 - ancho_total//2 + i * (ficha.ancho + espacio_entre_fichas)
                y = HEIGHT - margen - ficha.alto
                ficha.dibujar(x, y, False)
                indice_ficha += 1
            
            # LADO IZQUIERDO (vertical)
            for i in range(lados["izquierda"]):
                if indice_ficha >= total_fichas:
                    break
                ficha = self.fichas[indice_ficha]
                ficha.rotada = True
                alto_total = lados["izquierda"] * ficha.ancho + (lados["izquierda"] - 1) * espacio_entre_fichas
                x = margen
                y = HEIGHT//2 - alto_total//2 + i * (ficha.ancho + espacio_entre_fichas)
                ficha.dibujar(x, y, True)
                indice_ficha += 1

# Clase Juego de Dominó Premium
class JuegoDomino:
    def __init__(self):
        self.mesa = Mesa()
        self.jugadores = []
        self.monton = []
        self.turno_actual = 0
        self.estado = EstadoJuego.MENU
        self.ganador = None
        self.sentido_horario = True
        self.ficha_seleccionada = None
        self.num_jugadores_humanos = 1
        self.num_jugadores_totales = 4
        self.tiempo_ultima_jugada = 0
        self.mostrar_ayuda = True
    
    def crear_fichas(self):
        fichas = []
        for i in range(7):
            for j in range(i, 7):
                fichas.append(Ficha(i, j))
        random.shuffle(fichas)
        return fichas
    
    def configurar_jugadores(self, humanos, totales):
        self.num_jugadores_humanos = humanos
        self.num_jugadores_totales = totales
        self.jugadores = []
        
        # Crear jugadores humanos
        for i in range(humanos):
            self.jugadores.append(Jugador(f"Jugador {i+1}", es_humano=True))
        
        # Crear jugadores CPU
        for i in range(humanos, totales):
            dificultad = random.choice(["fácil", "normal", "difícil"])
            self.jugadores.append(Jugador(f"CPU {i+1-humanos}", es_humano=False, dificultad=dificultad))
    
    def repartir_fichas(self):
        self.monton = self.crear_fichas()
        
        # Calcular fichas por jugador
        fichas_por_jugador = 7 if self.num_jugadores_totales <= 4 else 5
        
        # Repartir fichas a cada jugador
        for jugador in self.jugadores:
            jugador.fichas = []
            for _ in range(fichas_por_jugador):
                if self.monton:
                    jugador.agregar_ficha(self.monton.pop())
        
        # Ordenar fichas de cada jugador
        for jugador in self.jugadores:
            jugador.fichas.sort(key=lambda f: (f.izquierda, f.derecha))
    
    def encontrar_iniciador(self):
        # Buscar el doble más alto
        dobles = []
        for i, jugador in enumerate(self.jugadores):
            for ficha in jugador.fichas:
                if ficha.es_doble():
                    dobles.append((ficha.izquierda, i))
        
        if dobles:
            doble_mas_alto = max(dobles, key=lambda x: x[0])
            return doble_mas_alto[1]
        
        # Si no hay dobles, buscar la ficha con más puntos
        max_puntos = -1
        jugador_iniciador = 0
        for i, jugador in enumerate(self.jugadores):
            for ficha in jugador.fichas:
                if ficha.valor_total() > max_puntos:
                    max_puntos = ficha.valor_total()
                    jugador_iniciador = i
        
        return jugador_iniciador
    
    def iniciar_juego(self):
        self.repartir_fichas()
        self.turno_actual = self.encontrar_iniciador()
        
        # Colocar la primera ficha
        jugador_inicial = self.jugadores[self.turno_actual]
        if any(ficha.es_doble() for ficha in jugador_inicial.fichas):
            doble_mas_alto = max([f for f in jugador_inicial.fichas if f.es_doble()], 
                               key=lambda f: f.izquierda, default=None)
            ficha_inicial = doble_mas_alto
        else:
            ficha_inicial = max(jugador_inicial.fichas, key=lambda f: f.valor_total())
        
        jugador_inicial.remover_ficha(ficha_inicial)
        self.mesa.colocar_ficha_inicial(ficha_inicial)
        self.siguiente_turno()
        self.estado = EstadoJuego.JUGANDO
        self.tiempo_ultima_jugada = pygame.time.get_ticks()
    
    def siguiente_turno(self):
        if self.sentido_horario:
            self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
        else:
            self.turno_actual = (self.turno_actual - 1) % len(self.jugadores)
        
        # Actualizar fichas jugables para el nuevo jugador
        jugador_actual = self.jugador_actual()
        jugador_actual.buscar_fichas_jugables(
            self.mesa.extremo_izquierdo, self.mesa.extremo_derecho
        )
    
    def jugador_actual(self):
        return self.jugadores[self.turno_actual]
    
    def es_turno_humano(self):
        return self.jugador_actual().es_humano
    
    def jugada_valida(self, ficha, extremo):
        if extremo == "izquierda":
            return ficha.derecha == self.mesa.extremo_izquierdo or ficha.izquierda == self.mesa.extremo_izquierdo
        else:  # derecha
            return ficha.izquierda == self.mesa.extremo_derecho or ficha.derecha == self.mesa.extremo_derecho
    
    def realizar_jugada_humano(self, ficha, extremo):
        jugador = self.jugador_actual()
        
        if extremo == "izquierda":
            if self.mesa.colocar_ficha_izquierda(ficha):
                jugador.remover_ficha(ficha)
                self.tiempo_ultima_jugada = pygame.time.get_ticks()
                return True
        else:  # derecha
            if self.mesa.colocar_ficha_derecha(ficha):
                jugador.remover_ficha(ficha)
                self.tiempo_ultima_jugada = pygame.time.get_ticks()
                return True
        
        return False
    
    def realizar_jugada_cpu(self):
        jugador = self.jugador_actual()
        fichas_jugables = jugador.buscar_fichas_jugables(
            self.mesa.extremo_izquierdo, self.mesa.extremo_derecho
        )
        
        if not fichas_jugables:
            # Robar del montón
            if self.monton:
                ficha_robada = self.monton.pop()
                jugador.agregar_ficha(ficha_robada)
                return True
            else:
                # Pasar turno
                return True
        
        # Estrategia según dificultad
        if jugador.dificultad == "fácil":
            ficha_elegida = random.choice(fichas_jugables)
        elif jugador.dificultad == "normal":
            # Preferir fichas que no sean dobles
            fichas_no_dobles = [f for f in fichas_jugables if not f.es_doble()]
            ficha_elegida = random.choice(fichas_no_dobles) if fichas_no_dobles else random.choice(fichas_jugables)
        else:  # difícil
            # Preferir fichas con valores altos
            ficha_elegida = max(fichas_jugables, key=lambda f: f.valor_total())
        
        # Decidir en qué extremo colocarla
        puede_izquierda = self.jugada_valida(ficha_elegida, "izquierda")
        puede_derecha = self.jugada_valida(ficha_elegida, "derecha")
        
        if puede_izquierda and puede_derecha:
            extremo = random.choice(["izquierda", "derecha"])
        elif puede_izquierda:
            extremo = "izquierda"
        else:
            extremo = "derecha"
        
        # Realizar la jugada
        if extremo == "izquierda":
            self.mesa.colocar_ficha_izquierda(ficha_elegida)
        else:
            self.mesa.colocar_ficha_derecha(ficha_elegida)
        
        jugador.remover_ficha(ficha_elegida)
        self.tiempo_ultima_jugada = pygame.time.get_ticks()
        return True
    
    def verificar_fin_juego(self):
        # Verificar si algún jugador se quedó sin fichas
        for i, jugador in enumerate(self.jugadores):
            if not jugador.tiene_fichas():
                self.ganador = jugador
                self.estado = EstadoJuego.FINALIZADO
                return True
        
        # Verificar si el juego está trancado
        if not self.monton:
            jugadores_con_fichas = [j for j in self.jugadores if j.tiene_fichas()]
            if len(jugadores_con_fichas) > 1:
                alguien_puede_jugar = False
                for jugador in jugadores_con_fichas:
                    fichas_jugables = jugador.buscar_fichas_jugables(
                        self.mesa.extremo_izquierdo, self.mesa.extremo_derecho
                    )
                    if fichas_jugables:
                        alguien_puede_jugar = True
                        break
                
                if not alguien_puede_jugar:
                    # Juego trancado, gana el que tenga menos puntos
                    self.ganador = min(self.jugadores, key=lambda j: j.contar_puntos())
                    self.estado = EstadoJuego.FINALIZADO
                    return True
        
        return False
    
    def actualizar(self):
        if self.estado != EstadoJuego.JUGANDO:
            return
        
        self.mesa.actualizar_animaciones()
        
        if self.verificar_fin_juego():
            return
        
        # Jugar automáticamente si es CPU después de un breve retraso
        if not self.es_turno_humano():
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_ultima_jugada > 1500:  # 1.5 segundos de retraso
                self.realizar_jugada_cpu()
                self.siguiente_turno()

# Funciones de dibujo premium
def dibujar_texto(texto, x, y, tamaño=24, color=COLORES["BLANCO_PREMIUM"], fuente=None, centrado=False):
    if fuente is None:
        fuente = pygame.font.SysFont("Arial", tamaño)
    else:
        fuente = pygame.font.SysFont(fuente, tamaño)
    
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect()
    
    if centrado:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    
    screen.blit(superficie, rect)
    return rect

def dibujar_boton(texto, x, y, ancho, alto, color_base, color_texto=COLORES["BLANCO_PREMIUM"], hover=False):
    # Asegurar que los colores estén en el rango 0-255
    def clamp_color(value):
        return max(0, min(255, value))
    
    if hover:
        color = (clamp_color(color_base[0] + 30), 
                clamp_color(color_base[1] + 30), 
                clamp_color(color_base[2] + 30))
    else:
        color = color_base
    
    # Sombra del botón
    pygame.draw.rect(screen, COLORES["NEGRO_SUAVE"], (x+3, y+3, ancho, alto), border_radius=12)
    
    # Botón principal
    pygame.draw.rect(screen, color, (x, y, ancho, alto), border_radius=12)
    
    # Borde dorado
    pygame.draw.rect(screen, COLORES["ORO_PRINCIPAL"], (x, y, ancho, alto), 3, border_radius=12)
    
    # Efecto de brillo en la parte superior
    brillo_color = (clamp_color(color_base[0]+50), 
                   clamp_color(color_base[1]+50), 
                   clamp_color(color_base[2]+50))
    pygame.draw.rect(screen, brillo_color, 
                   (x+2, y+2, ancho-4, alto//4), border_radius=10)
    
    # Texto del botón
    dibujar_texto(texto, x + ancho//2, y + alto//2, 20, color_texto, centrado=True)
    
    return pygame.Rect(x, y, ancho, alto)

def dibujar_hud(juego):
    # Panel superior premium
    pygame.draw.rect(screen, COLORES["NEGRO_SUAVE"], (0, 0, WIDTH, 70))
    
    # Línea decorativa dorada
    pygame.draw.line(screen, COLORES["ORO_PRINCIPAL"], (0, 70), (WIDTH, 70), 3)
    
    # Información de jugadores
    for i, jugador in enumerate(juego.jugadores):
        x = 20 + i * 250
        y = 20
        
        # Dibujar avatar
        es_turno_actual = (i == juego.turno_actual)
        jugador.dibujar_avatar(x + 15, y + 15, es_turno_actual)
        
        # Información del jugador
        color_nombre = COLORES["ORO_CLARO"] if es_turno_actual else COLORES["BLANCO_PREMIUM"]
        
        # Ajustar posición según número de jugadores
        if len(juego.jugadores) > 3:
            x = 20 + i * (WIDTH - 40) // len(juego.jugadores)
            dibujar_texto(jugador.nombre[:8], x + 40, y, 14, color_nombre)
            info = f"{len(jugador.fichas)} fichas"
        else:
            dibujar_texto(jugador.nombre, x + 40, y, 16, color_nombre)
            info = f"Fichas: {len(jugador.fichas)}"
            if not jugador.es_humano:
                info += f" ({jugador.dificultad})"
        
        dibujar_texto(info, x + 40, y + 25, 14, COLORES["PLATA"])
    
    # Información de la mesa
    if juego.mesa.extremo_izquierdo is not None and juego.mesa.extremo_derecho is not None:
        texto_extremos = f"Extremos: {juego.mesa.extremo_izquierdo} - {juego.mesa.extremo_derecho}"
        dibujar_texto(texto_extremos, WIDTH - 200, 25, 18, COLORES["BLANCO_PREMIUM"])
    
    # Montón de fichas
    dibujar_texto(f"Montón: {len(juego.monton)}", WIDTH - 100, 45, 16, COLORES["PLATA"])
    
    # Botón de ayuda
    if juego.mostrar_ayuda:
        boton_ayuda = dibujar_boton("?", WIDTH - 50, 15, 30, 30, COLORES["AZUL_LUJO"], hover=False)
        return boton_ayuda
    return None

def dibujar_fichas_jugador(juego):
    jugador = juego.jugador_actual()
    if not jugador.es_humano:
        return
    
    # Panel inferior premium
    pygame.draw.rect(screen, COLORES["NEGRO_SUAVE"], (0, HEIGHT - 180, WIDTH, 180))
    pygame.draw.line(screen, COLORES["ORO_PRINCIPAL"], (0, HEIGHT - 180), (WIDTH, HEIGHT - 180), 3)
    
    # Calcular posición para las fichas del jugador
    espacio_entre_fichas = 10
    ancho_total = len(jugador.fichas) * (jugador.fichas[0].ancho + espacio_entre_fichas) - espacio_entre_fichas
    inicio_x = max(20, (WIDTH - ancho_total) // 2)
    y = HEIGHT - 160
    
    for i, ficha in enumerate(jugador.fichas):
        x = inicio_x + i * (ficha.ancho + espacio_entre_fichas)
        ficha.dibujar(x, y)
        
        # Indicador visual premium para fichas jugables
        if ficha.jugable:
            pygame.draw.rect(screen, COLORES["ORO_CLARO"], (x-3, y-3, ficha.ancho+6, ficha.alto+6), 3, border_radius=12)

def dibujar_menu_principal(juego):
    # Fondo premium (terciopelo negro con patrón sutil)
    screen.fill(COLORES["NEGRO_LUJO"])
    
    # Patrón de diamantes sutil
    for i in range(0, WIDTH, 80):
        for j in range(0, HEIGHT, 80):
            color_patron = (*COLORES["NEGRO_SUAVE"], 10)
            surf_patron = pygame.Surface((80, 80), pygame.SRCALPHA)
            puntos = [(40, 0), (80, 40), (40, 80), (0, 40)]
            pygame.draw.polygon(surf_patron, color_patron, puntos)
            screen.blit(surf_patron, (i, j))
    
    # Título principal con efecto premium
    titulo_y = 120
    
    # Sombra del título
    for offset in range(3, 0, -1):
        dibujar_texto("DOMINÓ DE LUJO", WIDTH//2 + offset, titulo_y + offset, 80, 
                     COLORES["NEGRO_CARTA"], "Arial", True)
    
    # Título principal dorado
    dibujar_texto("DOMINÓ DE LUJO", WIDTH//2, titulo_y, 80, COLORES["ORO_PRINCIPAL"], "Arial", True)
    
    # Subtítulo
    dibujar_texto("EXPERIENCIA PREMIUM", WIDTH//2, titulo_y + 90, 36, COLORES["PLATA"], "Arial", True)
    
    # Botones del menú principal
    boton_y = 350
    espacio_botones = 90
    
    mouse_pos = pygame.mouse.get_pos()
    
    boton_jugar = dibujar_boton("NUEVA PARTIDA", WIDTH//2 - 175, boton_y, 350, 70, COLORES["VERDE_LUJO"], 
                               hover=pygame.Rect(WIDTH//2 - 175, boton_y, 350, 70).collidepoint(mouse_pos))
    
    boton_config = dibujar_boton("CONFIGURACIÓN", WIDTH//2 - 175, boton_y + espacio_botones, 350, 70, COLORES["AZUL_LUJO"],
                                hover=pygame.Rect(WIDTH//2 - 175, boton_y + espacio_botones, 350, 70).collidepoint(mouse_pos))
    
    boton_salir = dibujar_boton("SALIR", WIDTH//2 - 175, boton_y + espacio_botones * 2, 350, 70, COLORES["ROJO_LUJO"],
                               hover=pygame.Rect(WIDTH//2 - 175, boton_y + espacio_botones * 2, 350, 70).collidepoint(mouse_pos))
    
    # Efectos visuales de partículas doradas
    if random.random() < 0.03:
        x = random.randint(100, WIDTH-100)
        y = random.randint(100, HEIGHT-100)
        crear_particulas(x, y, COLORES["ORO_CLARO"], 5)
    
    return boton_jugar, boton_config, boton_salir

def dibujar_seleccion_jugadores(juego):
    # Fondo premium
    screen.fill(COLORES["NEGRO_LUJO"])
    
    # Título
    dibujar_texto("CONFIGURACIÓN PREMIUM", WIDTH//2, 80, 48, COLORES["ORO_PRINCIPAL"], "Arial", True)
    
    mouse_pos = pygame.mouse.get_pos()
    
    # Selector de jugadores humanos
    dibujar_texto("Jugadores Humanos:", WIDTH//2 - 200, 200, 32, COLORES["BLANCO_PREMIUM"])
    boton_humanos_menos = dibujar_boton("-", WIDTH//2, 190, 50, 50, COLORES["ROJO_LUJO"],
                                       hover=pygame.Rect(WIDTH//2, 190, 50, 50).collidepoint(mouse_pos))
    boton_humanos_mas = dibujar_boton("+", WIDTH//2 + 100, 190, 50, 50, COLORES["VERDE_LUJO"],
                                     hover=pygame.Rect(WIDTH//2 + 100, 190, 50, 50).collidepoint(mouse_pos))
    
    # Selector de jugadores totales
    dibujar_texto("Jugadores Totales:", WIDTH//2 - 200, 300, 32, COLORES["BLANCO_PREMIUM"])
    boton_totales_menos = dibujar_boton("-", WIDTH//2, 290, 50, 50, COLORES["ROJO_LUJO"],
                                       hover=pygame.Rect(WIDTH//2, 290, 50, 50).collidepoint(mouse_pos))
    boton_totales_mas = dibujar_boton("+", WIDTH//2 + 100, 290, 50, 50, COLORES["VERDE_LUJO"],
                                     hover=pygame.Rect(WIDTH//2 + 100, 290, 50, 50).collidepoint(mouse_pos))
    
    # Mostrar configuración actual
    dibujar_texto(f"{juego.num_jugadores_humanos}", WIDTH//2 + 50, 215, 36, COLORES["ORO_CLARO"], "Arial", True)
    dibujar_texto(f"{juego.num_jugadores_totales}", WIDTH//2 + 50, 315, 36, COLORES["ORO_CLARO"], "Arial", True)
    
    # Información
    info_texto = f"Configuración: {juego.num_jugadores_humanos} humano(s) + " \
                f"{juego.num_jugadores_totales - juego.num_jugadores_humanos} CPU(s)"
    dibujar_texto(info_texto, WIDTH//2, 400, 24, COLORES["PLATA"], "Arial", True)
    
    # Botones de acción
    boton_iniciar = dibujar_boton("INICIAR PARTIDA", WIDTH//2 - 175, 500, 350, 70, COLORES["VERDE_LUJO"],
                                 hover=pygame.Rect(WIDTH//2 - 175, 500, 350, 70).collidepoint(mouse_pos))
    boton_volver = dibujar_boton("VOLVER AL MENÚ", WIDTH//2 - 175, 590, 350, 70, COLORES["AZUL_LUJO"],
                                hover=pygame.Rect(WIDTH//2 - 175, 590, 350, 70).collidepoint(mouse_pos))
    
    return (boton_humanos_menos, boton_humanos_mas, 
            boton_totales_menos, boton_totales_mas,
            boton_iniciar, boton_volver)

def dibujar_pantalla_final(juego):
    # Superposición semitransparente elegante
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    s.fill((0, 0, 0, 200))
    screen.blit(s, (0, 0))
    
    # Panel de resultados premium
    panel = pygame.Rect(WIDTH//2 - 350, HEIGHT//2 - 250, 700, 500)
    pygame.draw.rect(screen, COLORES["NEGRO_SUAVE"], panel, border_radius=25)
    pygame.draw.rect(screen, COLORES["ORO_PRINCIPAL"], panel, 5, border_radius=25)
    
    # Título
    if juego.ganador:
        color_titulo = juego.ganador.avatar_color
        titulo = f"¡{juego.ganador.nombre} GANA!"
    else:
        color_titulo = COLORES["ORO_CLARO"]
        titulo = "¡PARTIDA TERMINADA!"
    
    dibujar_texto(titulo, WIDTH//2, HEIGHT//2 - 200, 42, color_titulo, "Arial", True)
    
    # Tabla de resultados
    cabeza_y = HEIGHT//2 - 140
    dibujar_texto("JUGADOR", WIDTH//2 - 250, cabeza_y, 24, COLORES["ORO_PRINCIPAL"])
    dibujar_texto("FICHAS", WIDTH//2, cabeza_y, 24, COLORES["ORO_PRINCIPAL"])
    dibujar_texto("PUNTOS", WIDTH//2 + 250, cabeza_y, 24, COLORES["ORO_PRINCIPAL"])
    
    # Línea separadora
    pygame.draw.line(screen, COLORES["ORO_SECUNDARIO"], 
                   (WIDTH//2 - 350, cabeza_y + 20), (WIDTH//2 + 350, cabeza_y + 20), 2)
    
    # Resultados de cada jugador
    for i, jugador in enumerate(juego.jugadores):
        y = cabeza_y + 40 + i * 40
        
        # Nombre con avatar pequeño
        jugador.dibujar_avatar(WIDTH//2 - 280, y, False)
        dibujar_texto(jugador.nombre, WIDTH//2 - 250, y, 20, 
                     COLORES["ORO_CLARO"] if jugador == juego.ganador else COLORES["BLANCO_PREMIUM"])
        
        # Fichas restantes
        dibujar_texto(str(len(jugador.fichas)), WIDTH//2, y, 20, COLORES["BLANCO_PREMIUM"], "Arial", True)
        
        # Puntos
        puntos = jugador.contar_puntos()
        dibujar_texto(str(puntos), WIDTH//2 + 250, y, 20, COLORES["BLANCO_PREMIUM"], "Arial", True)
    
    mouse_pos = pygame.mouse.get_pos()
    
    # Botones
    boton_reiniciar = dibujar_boton("JUGAR OTRA VEZ", WIDTH//2 - 160, HEIGHT//2 + 150, 320, 60, COLORES["VERDE_LUJO"],
                                   hover=pygame.Rect(WIDTH//2 - 160, HEIGHT//2 + 150, 320, 60).collidepoint(mouse_pos))
    boton_menu = dibujar_boton("MENÚ PRINCIPAL", WIDTH//2 - 160, HEIGHT//2 + 230, 320, 60, COLORES["AZUL_LUJO"],
                              hover=pygame.Rect(WIDTH//2 - 160, HEIGHT//2 + 230, 320, 60).collidepoint(mouse_pos))
    
    return boton_reiniciar, boton_menu

def dibujar_ayuda():
    panel = pygame.Rect(WIDTH//2 - 300, HEIGHT//2 - 200, 600, 400)
    pygame.draw.rect(screen, COLORES["NEGRO_SUAVE"], panel, border_radius=20)
    pygame.draw.rect(screen, COLORES["ORO_PRINCIPAL"], panel, 4, border_radius=20)
    
    titulo_y = HEIGHT//2 - 180
    dibujar_texto("CÓMO JUGAR AL DOMINÓ", WIDTH//2, titulo_y, 28, COLORES["ORO_CLARO"], "Arial", True)
    
    instrucciones = [
        "• El objetivo es quedarse sin fichas",
        "• Coloca fichas que coincidan con los extremos",
        "• Haz click en una ficha jugable para colocarla",
        "• Las fichas jugables se resaltan en dorado",
        "• Si no puedes jugar, robas del montón",
        "• Gana quien se quede sin fichas primero",
        "• O quien tenga menos puntos si el juego se tranca"
    ]
    
    for i, linea in enumerate(instrucciones):
        dibujar_texto(linea, WIDTH//2 - 250, titulo_y + 60 + i * 30, 18, COLORES["BLANCO_PREMIUM"])
    
    mouse_pos = pygame.mouse.get_pos()
    boton_cerrar = dibujar_boton("ENTENDIDO", WIDTH//2, HEIGHT//2 + 120, 200, 50, COLORES["VERDE_LUJO"],
                                hover=pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 95, 200, 50).collidepoint(mouse_pos))
    return boton_cerrar

# Función principal premium
def main():
    clock = pygame.time.Clock()
    juego = JuegoDomino()
    
    # Configuración predeterminada
    juego.configurar_jugadores(1, 4)
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if juego.estado == EstadoJuego.JUGANDO:
                        juego.estado = EstadoJuego.MENU
                    elif juego.estado == EstadoJuego.SELECCION_JUGADORES:
                        juego.estado = EstadoJuego.MENU
                    else:
                        running = False
                
                if event.key == pygame.K_h:
                    juego.mostrar_ayuda = not juego.mostrar_ayuda
        
        # Actualizar partículas
        global particulas
        particulas = [p for p in particulas if p.update()]
        
        # Dibujar según el estado del juego
        if juego.estado == EstadoJuego.MENU:
            boton_jugar, boton_config, boton_salir = dibujar_menu_principal(juego)
            
            if mouse_click:
                if boton_jugar.collidepoint(mouse_pos):
                    juego.iniciar_juego()
                elif boton_config.collidepoint(mouse_pos):
                    juego.estado = EstadoJuego.SELECCION_JUGADORES
                elif boton_salir.collidepoint(mouse_pos):
                    running = False
        
        elif juego.estado == EstadoJuego.SELECCION_JUGADORES:
            (boton_h_menos, boton_h_mas, 
             boton_t_menos, boton_t_mas,
             boton_iniciar, boton_volver) = dibujar_seleccion_jugadores(juego)
            
            if mouse_click:
                if boton_h_menos.collidepoint(mouse_pos) and juego.num_jugadores_humanos > 1:
                    juego.num_jugadores_humanos -= 1
                elif boton_h_mas.collidepoint(mouse_pos) and juego.num_jugadores_humanos < juego.num_jugadores_totales:
                    juego.num_jugadores_humanos += 1
                elif boton_t_menos.collidepoint(mouse_pos) and juego.num_jugadores_totales > max(2, juego.num_jugadores_humanos):
                    juego.num_jugadores_totales -= 1
                elif boton_t_mas.collidepoint(mouse_pos) and juego.num_jugadores_totales < 6:
                    juego.num_jugadores_totales += 1
                elif boton_iniciar.collidepoint(mouse_pos):
                    juego.configurar_jugadores(juego.num_jugadores_humanos, juego.num_jugadores_totales)
                    juego.iniciar_juego()
                elif boton_volver.collidepoint(mouse_pos):
                    juego.estado = EstadoJuego.MENU
        
        elif juego.estado == EstadoJuego.JUGANDO:
            # Actualizar lógica del juego
            juego.actualizar()
            
            # Dibujar juego
            juego.mesa.dibujar()
            boton_ayuda = dibujar_hud(juego)
            dibujar_fichas_jugador(juego)
            
            # Manejar interacción del jugador humano
            if mouse_click and juego.es_turno_humano():
                jugador = juego.jugador_actual()
                
                # Verificar clic en fichas del jugador
                for ficha in jugador.fichas:
                    rect = ficha.get_rect()
                    if rect.collidepoint(mouse_pos) and ficha.jugable:
                        # Intentar colocar en ambos extremos
                        if juego.jugada_valida(ficha, "izquierda"):
                            if juego.realizar_jugada_humano(ficha, "izquierda"):
                                juego.siguiente_turno()
                                break
                        elif juego.jugada_valida(ficha, "derecha"):
                            if juego.realizar_jugada_humano(ficha, "derecha"):
                                juego.siguiente_turno()
                                break
                
                # Verificar clic en botón de ayuda
                if boton_ayuda and boton_ayuda.collidepoint(mouse_pos):
                    juego.mostrar_ayuda = not juego.mostrar_ayuda
            
            # Mostrar ayuda si está activada
            if juego.mostrar_ayuda:
                boton_cerrar_ayuda = dibujar_ayuda()
                if mouse_click and boton_cerrar_ayuda.collidepoint(mouse_pos):
                    juego.mostrar_ayuda = False
        
        elif juego.estado == EstadoJuego.FINALIZADO:
            # Dibujar juego de fondo
            juego.mesa.dibujar()
            dibujar_hud(juego)
            
            # Dibujar pantalla final
            boton_reiniciar, boton_menu = dibujar_pantalla_final(juego)
            
            if mouse_click:
                if boton_reiniciar.collidepoint(mouse_pos):
                    juego.configurar_jugadores(juego.num_jugadores_humanos, juego.num_jugadores_totales)
                    juego.iniciar_juego()
                elif boton_menu.collidepoint(mouse_pos):
                    juego.estado = EstadoJuego.MENU
        
        # Dibujar partículas
        for particula in particulas:
            particula.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()