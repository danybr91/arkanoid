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
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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

for row in range(6):
    for col in range(10):
        brick_x = col * (BRICK_WIDTH + 10) + 35
        brick_y = row * (BRICK_HEIGHT + 10) + 50
        bricks.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))

# Variables de puntuación y vidas
score = 0
lives = INITIAL_LIVES
font = pygame.font.Font(None, FONT_SIZE)

# Variable de pausa (comenzar en pausa)
paused = True

# Variable para indicar si el juego ha terminado
game_over = False

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
    for brick in bricks:
        pygame.draw.rect(screen, GREEN, brick)

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

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Movimiento con flechas
            if event.key == pygame.K_LEFT:
                paddle_dx = -PADDLE_SPEED
            elif event.key == pygame.K_RIGHT:
                paddle_dx = PADDLE_SPEED
            # Movimiento con teclas A y D
            elif event.key == pygame.K_a:
                paddle_dx = -PADDLE_SPEED
            elif event.key == pygame.K_d:
                paddle_dx = PADDLE_SPEED
            elif event.key == pygame.K_p and not game_over:  # Tecla para pausar/despausar (solo si no es game over)
                paused = not paused
            elif event.key == pygame.K_r and game_over:  # Tecla para reiniciar (solo si es game over)
                # Reiniciar el juego
                lives = INITIAL_LIVES
                score = 0
                reset_paddle()
                reset_ball()
                game_over = False
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
        elif ball_y == paddle_y - BALL_WIDTH and lives == INITIAL_LIVES:
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

    # Actualización de la posición de la paleta
    paddle_x += paddle_dx
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
    if paddle_y < ball_y + BALL_WIDTH and paddle_y + PADDLE_HEIGHT > ball_y:
        if paddle_x < ball_x + BALL_WIDTH and paddle_x + PADDLE_WIDTH > ball_x:
            ball_dy = -ball_dy

    # Colisión con los ladrillos
    for brick in bricks[:]:
        if brick.colliderect(pygame.Rect(ball_x, ball_y, BALL_WIDTH, BALL_WIDTH)):
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
        elif ball_y == paddle_y - BALL_WIDTH and lives == INITIAL_LIVES:
            draw_pause(START_MESSAGE)  # Mensaje inicial
        else:
            draw_pause(PAUSE_MESSAGE)  # Mensaje de pausa normal
    pygame.display.flip()

    # Control de FPS
    clock.tick(FPS)

pygame.quit()
