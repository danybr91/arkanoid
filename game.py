import pygame
import random

# Inicialización de pygame
pygame.init()

# Dimensiones de la pantalla
screen_width = 800
screen_height = 600

# Colores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Crear la pantalla
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Juego de Romper Ladrillos")

# Reloj para controlar la velocidad de actualización de la pantalla
clock = pygame.time.Clock()

# Variables de la pelota
ball_width = 10
ball_x = screen_width // 2 - ball_width // 2
ball_y = screen_height // 2 - ball_width // 2
ball_dx = 3
ball_dy = 3
ball_speed_increase = 2  # Aumento de velocidad cuando se pulsa 'C'

# Variables de la paleta
paddle_width = 100
paddle_height = 10
paddle_x = screen_width // 2 - paddle_width // 2
paddle_y = screen_height - 40
paddle_dx = 0
paddle_speed = 5

# Variables de los ladrillos
brick_width = 75
brick_height = 20
bricks = []

for row in range(6):
    for col in range(10):
        brick_x = col * (brick_width + 10) + 35
        brick_y = row * (brick_height + 10) + 50
        bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))

# Variables de puntuación y vidas
score = 0
lives = 3  # Número de vidas
font = pygame.font.Font(None, 36)

# Variable de pausa
paused = False

# Función para dibujar la pelota
def draw_ball():
    pygame.draw.ellipse(screen, white, [ball_x, ball_y, ball_width, ball_width])

# Función para dibujar la paleta
def draw_paddle():
    pygame.draw.rect(screen, blue, [paddle_x, paddle_y, paddle_width, paddle_height])

# Función para dibujar los ladrillos
def draw_bricks():
    for brick in bricks:
        pygame.draw.rect(screen, green, brick)

# Función para dibujar la puntuación
def draw_score():
    score_text = font.render(f"Puntuación: {score}", True, white)
    screen.blit(score_text, [10, 10])

# Función para dibujar las vidas
def draw_lives():
    lives_text = font.render(f"Vidas: {lives}", True, white)
    screen.blit(lives_text, [screen_width - 100, 10])

# Función para reiniciar la posición de la pelota
def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    # Posicionar la pelota justo encima de la paleta
    ball_x = paddle_x + paddle_width // 2 - ball_width // 2
    ball_y = paddle_y - ball_width
    # La pelota siempre va hacia arriba al reiniciar
    ball_dx = 3 * random.choice([-1, 1])
    ball_dy = -3  # Siempre hacia arriba

# Función para mostrar el mensaje de pausa
def draw_pause():
    pause_text = font.render("PAUSA - Presiona 'P' para continuar", True, white)
    text_rect = pause_text.get_rect(center=(screen_width//2, screen_height//2))
    screen.blit(pause_text, text_rect)

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle_dx = -paddle_speed
            elif event.key == pygame.K_RIGHT:
                paddle_dx = paddle_speed
            elif event.key == pygame.K_p:  # Tecla para pausar/despausar
                paused = not paused
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                paddle_dx = 0

    # Si el juego está pausado, solo dibujamos y continuamos el bucle
    if paused:
        # Dibujar todo
        screen.fill(black)
        draw_ball()
        draw_paddle()
        draw_bricks()
        draw_score()
        draw_lives()
        draw_pause()  # Mostrar mensaje de pausa
        pygame.display.flip()
        clock.tick(60)
        continue  # Saltar el resto de la lógica del juego

    # Verificar si se está presionando 'C'
    keys = pygame.key.get_pressed()
    if keys[pygame.K_c]:
        current_ball_dx = ball_dx * ball_speed_increase
        current_ball_dy = ball_dy * ball_speed_increase
    else:
        current_ball_dx = ball_dx
        current_ball_dy = ball_dy

    # Actualización de la posición de la paleta
    paddle_x += paddle_dx
    if paddle_x < 0:
        paddle_x = 0
    elif paddle_x > screen_width - paddle_width:
        paddle_x = screen_width - paddle_width

    # Actualización de la posición de la pelota
    ball_x += current_ball_dx
    ball_y += current_ball_dy

    if ball_x <= 0 or ball_x >= screen_width - ball_width:
        ball_dx = -ball_dx
    if ball_y <= 0:
        ball_dy = -ball_dy
    if ball_y >= screen_height - ball_width:
        # En lugar de terminar el juego, restar una vida y reiniciar la pelota
        lives -= 1
        if lives <= 0:
            running = False  # Fin del juego si no quedan vidas
        else:
            reset_ball()

    # Colisión con la paleta
    if paddle_y < ball_y + ball_width and paddle_y + paddle_height > ball_y:
        if paddle_x < ball_x + ball_width and paddle_x + paddle_width > ball_x:
            ball_dy = -ball_dy

    # Colisión con los ladrillos
    for brick in bricks[:]:
        if brick.colliderect(pygame.Rect(ball_x, ball_y, ball_width, ball_width)):
            bricks.remove(brick)
            ball_dy = -ball_dy
            score += 10  # Incrementar puntuación al destruir un ladrillo
            break

    # Dibujar todo
    screen.fill(black)
    draw_ball()
    draw_paddle()
    draw_bricks()
    draw_score()
    draw_lives()  # Dibujar las vidas
    # Mostrar indicador de pausa si el juego está en pausa
    if paused:
        draw_pause()
    pygame.display.flip()

    # Control de FPS
    clock.tick(60)

pygame.quit()
