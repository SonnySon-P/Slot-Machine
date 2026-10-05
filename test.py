import pygame
import random
import sys

WIDTH = 900
HEIGHT = 650
FPS = 60

BACKGROUND_COLOR = (0, 0, 0)
MACHINE_COLOR = (25, 28, 38)
WHITE_COLOR = (245, 245, 245)
BLACK_COLOR = (10, 10, 10)
RED_COLOR = (220, 60, 60)
GREEN_COLOR = (70, 210, 120)
GREY_COLOR = (100, 100, 100)
YELLOW_COLOR = (245, 205, 70)
BLUE_COLOR = (70, 150, 240)
PURPLE_COLOR = (160, 90, 220)

DIGIT_BACKGROUND_COLOR = (15, 18, 22)
DIGIT_COLOR = (80, 255, 140)
DIGIT_BORDER_COLOR = (120, 130, 140)

BET = 1
REEL_WIDTH = 200
REEL_HEIGHT = 200
REEL_X = [WIDTH // 2 - 250 - REEL_WIDTH // 2, WIDTH // 2 - REEL_WIDTH // 2, WIDTH // 2 + 250 - REEL_WIDTH // 2]
REEL_Y = 180

SYMBOLS = ["CHERRY", "LEMON", "BELL", "STAR", "BAR", "7"]
PAYOUTS = {"CHERRY": 10, "LEMON": 8, "BELL": 12, "STAR": 20, "BAR": 40, "7": 100}
SYMBOL_FILES = {"CHERRY": "cherry.png", "LEMON": "lemon.png", "BELL": "bell.png", "STAR": "star.png", "BAR": "bar.png", "7": "7.png"}

reel_positions = [0.0, 0.0, 0.0]
reel_speeds = [0.0, 0.0, 0.0]
reel_spinning = [False, False, False]
stop_times = [0, 0, 0]

coins = 100
spinning = False
result_symbols = ["CHERRY", "CHERRY", "CHERRY"]
message = "PRESS SPIN"
message_color = WHITE_COLOR
win_amount = 0

screen = None
font_big = None
font_medium = None
font_small = None
symbol_images = {}

spin_button = pygame.Rect(WIDTH // 2 + 250 - REEL_WIDTH // 2, 455, 200, 80)

def initialize():
    global screen, font_big, font_medium, font_small

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Slot Machine")

    font_big = pygame.font.SysFont("arial", 48, bold = True)
    font_medium = pygame.font.SysFont("arial", 36, bold = True)
    font_small = pygame.font.SysFont("arial", 28, bold = True)

    load_symbol_images()

def load_symbol_images():
    global symbol_images

    for symbol, filename in SYMBOL_FILES.items():
        try:
            image = pygame.image.load(filename).convert_alpha()
            symbol_images[symbol] = pygame.transform.smoothscale(image, (REEL_WIDTH, REEL_HEIGHT))

        except pygame.error as error:
            print(f"Unable to load image {filename}: {error}")
            pygame.quit()
            sys.exit()

def start_spin():
    global coins, spinning, message, message_color, win_amount

    if spinning:
        return

    if coins < BET:
        message = "NO COINS!"
        message_color = RED_COLOR
        return

    coins -= BET
    win_amount = 0
    message = "SPINNING..."
    message_color = WHITE_COLOR
    spinning = True

    current_time = pygame.time.get_ticks()

    for i in range(3):
        reel_spinning[i] = True
        reel_speeds[i] = random.uniform(0.25, 0.38)
        stop_times[i] = current_time + 3000 + i * 2000 + random.randint(0, 1000)

def stop_reel(i):
    reel_spinning[i] = False
    reel_positions[i] = round(reel_positions[i]) % len(SYMBOLS)

def get_reel_symbol(reel_index):
    position = int(round(reel_positions[reel_index])) % len(SYMBOLS)
    return SYMBOLS[position]

def check_result():
    global message, message_color, coins, win_amount, result_symbols, spinning

    result_symbols = [get_reel_symbol(0), get_reel_symbol(1), get_reel_symbol(2)]
    a, b, c = result_symbols

    if a == "7" and b == "7" and c == "7":
        win_amount = 500
        coins += win_amount
        message = "JACKPOT! 777!"
        message_color = YELLOW_COLOR

    elif a == b == c:
        win_amount = PAYOUTS[a]
        coins += win_amount
        message = f"WIN! +{win_amount}"
        message_color = GREEN_COLOR

    elif [a, b, c].count("CHERRY") >= 2:
        win_amount = 5
        coins += win_amount
        message = f"CHERRY! +{win_amount}"
        message_color = RED_COLOR

    else:
        win_amount = 0
        message = "LOSE"
        message_color = WHITE_COLOR

    spinning = False

def draw_machine():
    screen.fill(BACKGROUND_COLOR)

    machine_rectangle = pygame.Rect(70, 70, WIDTH - 140, HEIGHT - 140)
    pygame.draw.rect(screen, MACHINE_COLOR, machine_rectangle, border_radius = 20)

    draw_text_with_outline("JACKPOT", font_big, YELLOW_COLOR, WHITE_COLOR, WIDTH // 2, 115)

    for i in range(3):
        draw_reel(i)

    draw_coin_display()
    draw_text(message, font_small, message_color, WIDTH // 2, 495)

    if spinning == True:
        button_color = GREY_COLOR

    else:
        button_color = GREEN_COLOR

    pygame.draw.rect(screen, button_color, spin_button, border_radius = 10)
    draw_text("SPIN", font_medium, WHITE_COLOR, spin_button.centerx, spin_button.centery)

def draw_text_with_outline(text, font, text_color, outline_color, x, y):
    text_surface = font.render(text, True, text_color)
    outline_surface = font.render(text, True, outline_color)
    
    width, height = text_surface.get_size()

    base_x = x - width // 2
    base_y = y - height // 2

    offsets = [
        (-2, 0), (2, 0), (0, -2), (0, 2),  # 上下左右
        (-2, -2), (2, -2), (-2, 2), (2, 2)  # 斜角
    ]

    for dx, dy in offsets:
        screen.blit(outline_surface, (base_x + dx, base_y + dy))

    screen.blit(text_surface, (base_x, base_y))

def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    rectangle = surface.get_rect(center = (x, y))
    screen.blit(surface, rectangle)

def draw_reel(reel_index):
    x = REEL_X[reel_index]
    symbol = get_reel_symbol(reel_index)
    draw_symbol(symbol, x, REEL_Y)

def draw_symbol(symbol, x, y):
    rectangle_1 = pygame.Rect(x - 10, y - 10, REEL_WIDTH + 10 * 2, REEL_HEIGHT + 10 * 2)
    pygame.draw.rect(screen, WHITE_COLOR, rectangle_1, width = 3)

    rectangle_2 = pygame.Rect(x, y, REEL_WIDTH, REEL_HEIGHT)
    pygame.draw.rect(screen, WHITE_COLOR, rectangle_2)
    
    image = symbol_images[symbol]
    screen.blit(image, rectangle_2)

def draw_coin_display():
    display_rectangle = pygame.Rect(WIDTH // 2 - 250 - REEL_WIDTH // 2, 455, 200, 80)

    pygame.draw.rect(screen, BLACK_COLOR, display_rectangle, border_radius = 6)
    pygame.draw.rect(screen, DIGIT_BORDER_COLOR, display_rectangle, width = 3, border_radius = 6)

    inner_rectangle = pygame.Rect(
        display_rectangle.x + 8,
        display_rectangle.y + 8,
        display_rectangle.width - 16,
        display_rectangle.height - 16
    )

    pygame.draw.rect(screen, DIGIT_BACKGROUND_COLOR, inner_rectangle, border_radius = 3)

    coin_text = f"{max(0, min(coins, 9999)):04d}"
    digit_font = pygame.font.SysFont("couriernew", 60, bold = True)
    text_surface = digit_font.render(coin_text, True, DIGIT_COLOR)
    text_rectangle = text_surface.get_rect(center = inner_rectangle.center)
    screen.blit(text_surface, text_rectangle)

def update():
    if not spinning:
        return

    current_time = pygame.time.get_ticks()

    for i in range(3):
        if reel_spinning[i]:
            remaining = stop_times[i] - current_time

            if remaining <= 2000:
                slow_factor = max(0.08, remaining / 2000)
                current_speed = reel_speeds[i] * slow_factor

            else:
                current_speed = reel_speeds[i]

            reel_positions[i] += current_speed

            if remaining <= 0:
                stop_reel(i)

    if not any(reel_spinning):
        check_result()

def main():
    initialize()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if spin_button.collidepoint(event.pos):
                    start_spin()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_spin()

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        update()
        draw_machine()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
