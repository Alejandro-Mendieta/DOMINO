# 🎯 Dominó de Lujo - Juego Premium

![Dominó de Lujo](https://img.shields.io/badge/Estado-🚀%20Completo-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-orange)

Un juego de dominó elegante y sofisticado desarrollado en Python con Pygame, que combina la tradición del clásico juego de mesa con una experiencia visual premium.

## ✨ Características Principales

### 🎨 Diseño Premium
- **Paleta de colores dorada y negra** de lujo
- **Efectos visuales avanzados**: partículas doradas, sombras y brillos
- **Interfaz elegante** con bordes redondeados y gradientes sutiles
- **Animaciones fluidas** al colocar fichas

### 🎮 Experiencia de Juego
- **Distribución de fichas en forma de U** similar al dominó tradicional
- **Sistema de IA inteligente** con tres niveles de dificultad
- **Múltiples modos de juego**: 2-6 jugadores (humanos y CPU)
- **Sistema de ayuda integrado** con tutorial visual
- **Detectores de fichas jugables** con resaltado dorado

### ⚙️ Configuraciones Flexibles
- **Hasta 6 jugadores** en total
- **Combinación personalizable** de jugadores humanos y CPU
- **Dificultades ajustables**: Fácil, Normal y Difícil
- **Sistema de puntuación automático**

## 🛠️ Instalación y Requisitos

### Requisitos del Sistema
- **Python 3.8** o superior
- **Pygame 2.0** o superior
- **Sistema operativo**: Windows, macOS o Linux

### Instalación Rápida
```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/domino-lujo.git
cd domino-lujo

# Instalar dependencias
pip install pygame

# Ejecutar el juego
python domino_premium.py
```

### Instalación Manual
1. Descarga Python desde [python.org](https://python.org)
2. Instala Pygame: `pip install pygame`
3. Descarga el archivo `domino_premium.py`
4. Ejecuta: `python domino_premium.py`

## 🎯 Cómo Jugar

### Objetivo del Juego
- **Ser el primer jugador** en quedarse sin fichas
- **O tener la menor puntuación** si el juego se bloquea

### Reglas Básicas
1. **Coloca fichas** que coincidan con los números de los extremos
2. **Las fichas jugables** se resaltan en dorado
3. **Si no puedes jugar**, roba una ficha del montón
4. **Los dobles** se colocan perpendicularmente
5. **Gana** quien se quede sin fichas primero

### Controles
- **Clic izquierdo**: Seleccionar y colocar fichas
- **Tecla H**: Mostrar/ocultar ayuda
- **Tecla ESC**: Volver al menú principal
- **Botones de interfaz**: Navegación intuitiva

## 🎮 Modos de Juego

### Jugadores Humanos vs CPU
- **1-4 jugadores humanos** + CPUs para completar
- **CPU Fácil**: Decisiones aleatorias
- **CPU Normal**: Evita dobles cuando es posible
- **CPU Difícil**: Prioriza fichas de alto valor

### Configuraciones Populares
- **2 jugadores**: 1 humano vs 1 CPU
- **4 jugadores**: 2 humanos vs 2 CPUs
- **Partida completa**: 4 humanos
- **Práctica**: 1 humano vs 3 CPUs

## 🏆 Sistema de Puntuación

### Cálculo de Puntos
- **Victoria por fichas**: 0 puntos
- **Victoria por bloqueo**: Menor suma de puntos en fichas
- **Puntos por ficha**: Suma de ambos lados (0-12 puntos)

### Estrategias Avanzadas
- **Control de extremos**: Mantén opciones abiertas
- **Gestión de dobles**: Úsalos estratégicamente
- **Conteo de fichas**: Calcula probabilidades
- **Bloqueo táctico**: Forcejea cuando vayas ganando

## 🎨 Personalización

### Modificaciones Fáciles
```python
# Cambiar colores principales
COLORES["ORO_PRINCIPAL"] = (255, 200, 50)  # Dorado más brillante

# Ajustar tamaño de fichas
self.ancho = 100   # Más ancho
self.alto = 200    # Más alto

# Modificar velocidad de animación
anim["progreso"] += 0.05  # Más lento
```

### Distancia Entre Puntos
```python
# En _dibujar_puntos_premium:
espacio = 25  # Aumentar distancia entre puntos
radio = 10    # Aumentar tamaño de puntos
```

## 🐛 Solución de Problemas

### Problemas Comunes
```bash
# Error: Pygame no encontrado
pip install --upgrade pygame

# Error: Módulo no encontrado
python -m pip install pygame

# Rendimiento bajo
# Reducir efectos en sistemas limitados
```

### Optimizaciones
- **Sistemas lentos**: Desactivar partículas
- **Pantallas pequeñas**: Ajustar resolución
- **Problemas de sonido**: Verificar drivers de audio

## 📁 Estructura del Código

```
domino_premium.py
├── Clase Ficha (gestión visual y lógica de fichas)
├── Clase Jugador (humano y CPU)
├── Clase Mesa (distribución y animaciones)
├── Clase JuegoDomino (lógica principal)
├── Sistema de Partículas (efectos visuales)
└── Interfaces de Usuario (menús y HUD)
```

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Puedes:

1. **Reportar bugs** o sugerir mejoras
2. **Añadir nuevas características**
3. **Mejorar la IA** de los oponentes
4. **Crear temas visuales** alternativos
5. **Optimizar el rendimiento**

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 🎊 Créditos

**Desarrollado por:** **ALEJANDRO MENDIETA**
**Motor gráfico:** Pygame  
**Inspiración:** Juegos de dominó tradicionales  
**Diseño:** Paleta de colores premium dorado/negro

---

**¿Preguntas o sugerencias?**  
¡No dudes en abrir un issue o contactar al desarrollador!

---

<div align="center">

**🎲 ¡Disfruta del juego más elegante de dominó! 🎲**

</div>