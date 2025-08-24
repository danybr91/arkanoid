import pygame
import random

# AJUSTES GRÁFICOS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_SIZE = 36
FPS = 60

# AJUSTES DE JUEGO
INITIAL_LIVES = 3

# AJUSTES DE BOLA
BALL_WIDTH = 10
BALL_DX = 3
BALL_DY = 3
BALL_SPEED_INCREASE = 2

# AJUSTES DE PALA
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 5
PADDLE_SPEED_BOOST = 8  # Velocidad con boost (shift)

# AJUSTES DE BLOQUES
BRICK_WIDTH = 75
BRICK_HEIGHT = 20

# CONSTANTES DE TEXTO
GAME_TITLE = "Juego de Romper Ladrillos"
SCORE_TEXT = "Puntuación: {}"
LIVES_TEXT = "Vidas: {}"
PAUSE_MESSAGE = "PAUSA - Presiona 'P' para continuar"
START_MESSAGE = "Presiona 'P' para comenzar"
GAME_OVER_MESSAGE = "GAME OVER - Presiona 'R' para reiniciar o 'Q' para salir"

# COLORES (tuplas)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
INDIGO = (75, 0, 130)


# Colores para los ladrillos por filas
BRICK_COLORS = [
    RED,
    ORANGE,
    YELLOW,
    GREEN,
    BLUE,
    INDIGO
]

# Inicialización de pygame
pygame.init()

# Crear la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

# Reloj para controlar la velocidad de actualización de la pantalla
clock = pygame.time.Clock()

# Variables de la pelota
ball_x = SCREEN_WIDTH // 2 - BALL_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2 - BALL_WIDTH // 2
ball_dx = BALL_DX
ball_dy = BALL_DY

# Variables de la paleta
paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
paddle_y = SCREEN_HEIGHT - 40
paddle_dx = 0

# Variables de los ladrillos
bricks = []

# Posicionar la pelota en la paleta al inicio
ball_x = paddle_x + PADDLE_WIDTH // 2 - BALL_WIDTH // 2
ball_y = paddle_y - BALL_WIDTH

# Variables de puntuación y vidas
score = 0
lives = INITIAL_LIVES
font = pygame.font.Font(None, FONT_SIZE)

# Variable de pausa (comenzar en pausa)
paused = True

# Variable para indicar si el juego ha terminado
game_over = False

# Variable para indicar si es el inicio del juego
game_started = False

# Niveles

# Nivel 1
for row in range(6):
    for col in range(10):
        brick_x = col * (BRICK_WIDTH + 10) + 35
        brick_y = row * (BRICK_HEIGHT + 10) + 50
        brick_rect = pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append((brick_rect, BRICK_COLORS[row]))  # Almacenar rectángulo y color

# Función para resetear la posición de la paleta
def reset_paddle():
    global paddle_x
    paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2

# Función para dibujar la pelota
def draw_ball():
    pygame.draw.ellipse(screen, WHITE, [ball_x, ball_y, BALL_WIDTH, BALL_WIDTH])

# Función para dibujar la paleta
def draw_paddle():
    pygame.draw.rect(screen, BLUE, [paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT])

# Función para dibujar los ladrillos
def draw_bricks():
    for brick, color in bricks:
        pygame.draw.rect(screen, color, brick)

# Función para dibujar la puntuación
def draw_score():
    score_text = font.render(SCORE_TEXT.format(score), True, WHITE)
    screen.blit(score_text, [10, 10])

# Función para dibujar las vidas
def draw_lives():
    lives_text = font.render(LIVES_TEXT.format(lives), True, WHITE)
    screen.blit(lives_text, [SCREEN_WIDTH - 100, 10])

# Función para reiniciar la posición de la pelota
def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    # Posicionar la pelota justo encima de la paleta
    ball_x = paddle_x + PADDLE_WIDTH // 2 - BALL_WIDTH // 2
    ball_y = paddle_y - BALL_WIDTH
    # La pelota siempre va hacia arriba al reiniciar
    ball_dx = BALL_DX * random.choice([-1, 1])
    ball_dy = -BALL_DX  # Siempre hacia arriba

# Función para mostrar el mensaje de pausa
def draw_pause(message):
    pause_text = font.render(message, True, WHITE)
    text_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(pause_text, text_rect)

# Variables para el mensaje de depuración
debug_message = None
debug_ticks = 0

def draw_message(message, ticks):
    global debug_message, debug_ticks
    debug_message = message
    debug_ticks = ticks

def draw_debug_message():
    global debug_message, debug_ticks
    if debug_message and debug_ticks > 0:
        # Crear fuente para el mensaje de depuración (más pequeña que la fuente principal)
        debug_font = pygame.font.Font(None, 24)
        debug_text = debug_font.render(debug_message, True, RED)
        # Dibujar en la esquina inferior izquierda
        screen.blit(debug_text, [10, SCREEN_HEIGHT - 30])
        debug_ticks -= 1
        # Limpiar el mensaje cuando se agota el tiempo
        if debug_ticks <= 0:
            debug_message = None

def debug(event):
    global ball_dx,ball_dy
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_F1:
            ball_dy = -ball_dy
            draw_message("Invertido BALL DY", 60)
        if event.key == pygame.K_F2:
            ball_dx = -ball_dx
            draw_message("Invertido BALL DX", 60)

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        debug(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Movimiento con flechas
            if event.key == pygame.K_LEFT:
                paddle_dx = -1
            elif event.key == pygame.K_RIGHT:
                paddle_dx = 1
            # Movimiento con teclas A y D
            elif event.key == pygame.K_a:
                paddle_dx = -1
            elif event.key == pygame.K_d:
                paddle_dx = 1
            elif event.key == pygame.K_p and not game_over:  # Tecla para pausar/despausar (solo si no es game over)
                if not game_started:
                    game_started = True
                paused = not paused
            elif event.key == pygame.K_r and game_over:  # Tecla para reiniciar (solo si es game over)
                # Reiniciar el juego
                lives = INITIAL_LIVES
                score = 0
                reset_paddle()
                reset_ball()
                game_over = False
                game_started = False  # Reiniciar el estado del juego
                paused = True  # Volver a pausar al inicio
            elif event.key == pygame.K_q and game_over:  # Tecla para salir (solo si es game over)
                running = False
        elif event.type == pygame.KEYUP:
            # Detener movimiento con flechas
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                paddle_dx = 0
            # Detener movimiento con teclas A y D
            elif event.key == pygame.K_a or event.key == pygame.K_d:
                paddle_dx = 0

    # Si el juego está pausado, solo dibujamos y continuamos el bucle
    if paused:
        # Dibujar todo
        screen.fill(BLACK)
        # Solo dibujar la pelota si no es game over
        if not game_over:
            draw_ball()
        draw_paddle()
        draw_bricks()
        draw_score()
        draw_lives()
        # Mostrar mensaje apropiado según el estado del juego
        if game_over:
            draw_pause(GAME_OVER_MESSAGE)
        elif not game_started:
            draw_pause(START_MESSAGE)  # Mensaje inicial
        else:
            draw_pause(PAUSE_MESSAGE)  # Mensaje de pausa normal
        pygame.display.flip()
        clock.tick(FPS)
        continue  # Saltar el resto de la lógica del juego

    # Verificar si se está presionando 'C'
    keys = pygame.key.get_pressed()
    if keys[pygame.K_c]:
        current_ball_dx = ball_dx * BALL_SPEED_INCREASE
        current_ball_dy = ball_dy * BALL_SPEED_INCREASE
    else:
        current_ball_dx = ball_dx
        current_ball_dy = ball_dy

    # Determinar velocidad de la paleta según si se presiona SHIFT
    current_paddle_speed = PADDLE_SPEED_BOOST if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else PADDLE_SPEED

    # Actualización de la posición de la paleta
    paddle_x += paddle_dx * current_paddle_speed  # Ajustar velocidad según boost
    if paddle_x < 0:
        paddle_x = 0
    elif paddle_x > SCREEN_WIDTH - PADDLE_WIDTH:
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

    # Actualización de la posición de la pelota
    ball_x += current_ball_dx
    ball_y += current_ball_dy

    if ball_x <= 0 or ball_x >= SCREEN_WIDTH - BALL_WIDTH:
        ball_dx = -ball_dx
    if ball_y <= 0:
        ball_dy = -ball_dy
    if ball_y >= SCREEN_HEIGHT - BALL_WIDTH:
        # En lugar de terminar el juego, restar una vida y reiniciar la pelota y la paleta
        lives -= 1
        if lives <= 0:
            game_over = True  # Marcar que el juego ha terminado
            paused = True     # Pausar el juego
        else:
            reset_paddle()  # Resetear la posición de la paleta
            reset_ball()    # Resetear la posición de la pelota
            # Pausamos el juego
            paused = True

    # Colisión con la paleta
    paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball_rect = pygame.Rect(ball_x, ball_y, BALL_WIDTH, BALL_WIDTH)
    
    if paddle_rect.colliderect(ball_rect) and ball_dy > 0:
        # Calcular posición relativa del impacto en la paleta (de 0 a 1)
        relative_impact = (ball_x + BALL_WIDTH/2 - paddle_x) / PADDLE_WIDTH
        
        # Zona central plana (sin cambio de ángulo) - del 25% al 75% del ancho
        if 0.25 <= relative_impact <= 0.75:
            # Rebote vertical sin cambiar dirección horizontal
            ball_dy = -abs(ball_dy)
        else:
            # Zona de bordes redondeados - cambiar ángulo basado en posición
            bounce_angle = (relative_impact - 0.5) * 2
            
            # Mantener velocidad pero cambiar dirección
            speed = abs(ball_dy)
            ball_dx = bounce_angle * speed  # Componente horizontal
            ball_dy = -abs(ball_dy)  # Siempre hacia arriba
        
        # Asegurar que la pelota no se atasque en la paleta
        ball_y = paddle_y - BALL_WIDTH

    # Colisión con los ladrillos
    for brick in bricks[:]:
        if brick[0].colliderect(pygame.Rect(ball_x, ball_y, BALL_WIDTH, BALL_WIDTH)):
            bricks.remove(brick)
            ball_dy = -ball_dy
            score += 10  # Incrementar puntuación al destruir un ladrillo
            break

    # Dibujar todo
    screen.fill(BLACK)
    # Solo dibujar la pelota si no es game over
    if not game_over:
        draw_ball()

    draw_paddle()
    draw_bricks()
    draw_score()
    draw_lives()  # Dibujar las vidas
    # Mostrar indicador de pausa si el juego está en pausa
    if paused:
        if game_over:
            draw_pause(GAME_OVER_MESSAGE)
        elif not game_started:
            draw_pause(START_MESSAGE)  # Mensaje inicial
        else:
            draw_pause(PAUSE_MESSAGE)  # Mensaje de pausa normal
    
    # Dibujar mensaje de depuración si existe
    draw_debug_message()
    
    pygame.display.flip()

    # Control de FPS
    clock.tick(FPS)

pygame.quit()
