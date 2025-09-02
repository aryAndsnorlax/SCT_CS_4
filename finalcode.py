import pygame
import sys
import time

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Educational Keylogger Simulation")

# Fonts
font = pygame.font.SysFont("Arial", 24)
log_font = pygame.font.SysFont("Consolas", 18)

# Button class
class Button:
    def __init__(self, x, y, width, height, text):   # ✅ fixed constructor
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False

    def draw(self, surface, color, hover_color):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        fill_color = hover_color if self.hovered else color
        pygame.draw.rect(surface, fill_color, self.rect, border_radius=8)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.hovered

# Buttons
start_button = Button(50, 500, 180, 50, "Start Logging")
stop_button = Button(290, 500, 180, 50, "Stop Logging")
clear_button = Button(530, 500, 180, 50, "Clear Log")

# Log variables
logging_active = False
keystroke_log = []
log_file = None

# Open a new log file
def open_log_file():
    filename = f"keystroke_log_{time.strftime('%Y%m%d_%H%M%S')}.txt"
    return open(filename, "w")

# Draw keyboard layout (simplified)
def draw_keyboard():
    keys = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
    start_y = 150
    key_width, key_height = 50, 50
    spacing = 10

    for row_index, row in enumerate(keys):
        start_x = (WIDTH - (len(row) * (key_width + spacing))) // 2
        for col_index, key in enumerate(row):
            rect = pygame.Rect(start_x + col_index * (key_width + spacing),
                               start_y + row_index * (key_height + spacing),
                               key_width, key_height)
            pygame.draw.rect(screen, LIGHT_GRAY, rect, border_radius=5)
            key_surface = font.render(key, True, BLACK)
            key_rect = key_surface.get_rect(center=rect.center)
            screen.blit(key_surface, key_rect)

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Title
    title = font.render("Educational Keylogger Simulation", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

    # Draw UI
    draw_keyboard()
    start_button.draw(screen, GREEN, (0, 255, 0))
    stop_button.draw(screen, RED, (255, 0, 0))
    clear_button.draw(screen, BLUE, (0, 0, 255))

    # Display log preview
    log_label = font.render("Keystroke Log:", True, BLACK)
    screen.blit(log_label, (50, 420))
    log_preview = "".join(keystroke_log[-14:])  # last 14 chars
    log_surface = log_font.render(log_preview, True, BLACK)
    screen.blit(log_surface, (220, 425))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            if log_file:
                log_file.close()

        if start_button.is_clicked(event):
            if not logging_active:
                logging_active = True
                log_file = open_log_file()
                print("[INFO] Logging started.")

        if stop_button.is_clicked(event):
            if logging_active:
                logging_active = False
                if log_file:
                    log_file.close()
                    log_file = None
                print("[INFO] Logging stopped.")

        if clear_button.is_clicked(event):
            keystroke_log = []
            print("[INFO] Log cleared.")

        if event.type == pygame.KEYDOWN and logging_active:
            key_name = pygame.key.name(event.key)
            keystroke_log.append(key_name.upper())
            if log_file:
                log_file.write(key_name + "\n")

    pygame.display.flip()

pygame.quit()
sys.exit()
