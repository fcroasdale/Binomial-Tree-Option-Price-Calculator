# Binomial Option Pricing Model Visualization
# Author: Felix Croasdale, Saint Francis Xavier University
# Description: This script visualizes the binomial option pricing model using Pygame.

import math
import pygame

# ------------------------------
# User-defined Parameters (Inputs)
# ------------------------------

# Initial stock price
STOCK_PRICE = 40

# Exercise price of the option
EX_PRICE = 40

# Risk-free interest rate (in percent)
RISK_FREE_PCT = 4

# Number of time steps in the binomial model
TIME_STEPS = 101

# Time to maturity (in years)
TIME_TO_MATURITY = 6/12

# Volatility of the underlying asset (in percent)
VOLATILITY = 30

# Calculated parameters
DELTA_TIME_STEP = TIME_TO_MATURITY / TIME_STEPS
UPTICK = math.exp(VOLATILITY / 100 * math.sqrt(DELTA_TIME_STEP))
DOWNTICK = 1 / UPTICK

# ------------------------------
# Function Definitions
# ------------------------------

def option_tree(stock_price, ex_price, uptick, downtick, risk_free_pct, time_steps, delta_time_step):
    """Calculates the stock and option price tree for a European option."""
    risk_free_rate = risk_free_pct / 100
    discount_factor = math.exp(-risk_free_rate * delta_time_step)
    e = math.exp(risk_free_rate * delta_time_step)
    p = (e - downtick) / (uptick - downtick)

    stock_tree = [[0 for _ in range(step + 1)] for step in range(time_steps + 1)]
    option_tree = [[0 for _ in range(step + 1)] for step in range(time_steps + 1)]

    for step in range(time_steps + 1):
        for j in range(step + 1):
            stock_tree[step][j] = stock_price * (uptick ** j) * (downtick ** (step - j))

    for j in range(time_steps + 1):
        option_tree[time_steps][j] = max(0, stock_tree[time_steps][j] - ex_price)

    for step in range(time_steps - 1, -1, -1):
        for j in range(step + 1):
            up_value = option_tree[step + 1][j + 1]
            down_value = option_tree[step + 1][j]
            expected_value = p * up_value + (1 - p) * down_value
            option_tree[step][j] = max(0, discount_factor * expected_value)

    print("Option price at the root: ", option_tree[0][0])
    return stock_tree, option_tree

def draw_tree(screen, stock_tree, option_tree, height, time_steps, offset_x, offset_y, zoom):
    """Draws the binomial tree on a Pygame window."""
    font_size = int(12 * zoom)
    font = pygame.font.SysFont("Arial", font_size)
    max_text_width = 0
    for row in stock_tree:
        for value in row:
            text_width = font.size(f"S: {value:.2f}")[0]
            max_text_width = max(max_text_width, text_width)
    h_dist = max(max_text_width, 50) * zoom
    v_dist = max(30, height // (2 * time_steps)) * zoom
    node_radius = max(10, 20 * zoom)

    for step in range(time_steps + 1):
        for j in range(step + 1):
            x = offset_x + h_dist * step
            y = offset_y + v_dist * (step - 2 * j) + height // 2

            if step > 0:
                parent_x = offset_x + h_dist * (step - 1)
                parent_y_up = offset_y + v_dist * ((step - 1) - 2 * (j - 1)) + height // 2
                parent_y_down = offset_y + v_dist * ((step - 1) - 2 * j) + height // 2
                if j > 0:
                    pygame.draw.line(screen, (255, 255, 255), (x, y), (parent_x, parent_y_up))
                if j < step:
                    pygame.draw.line(screen, (255, 255, 255), (x, y), (parent_x, parent_y_down))

            pygame.draw.circle(screen, (0, 0, 255), (x, y), node_radius)
            stock_price_text = font.render(f"S: {stock_tree[step][j]:.2f}", True, (255, 255, 255))
            option_price_text = font.render(f"O: {option_tree[step][j]:.2f}", True, (255, 255, 255))
            text_x = x - 10 * zoom
            text_y_stock = y - 20 * zoom
            text_y_option = y + 10 * zoom
            screen.blit(stock_price_text, (text_x, text_y_stock))
            screen.blit(option_price_text, (text_x, text_y_option))

def visualize_binomial_tree(stock_price, ex_price, uptick, downtick, risk_free_pct, time_steps, delta_time_step):
    """Initializes Pygame and calls functions to build and draw the binomial tree."""
    pygame.init()
    width, height = 1080, 720
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Binomial Tree Visualization")

    # Zoom functionality variables
    zoom = 1.0
    min_zoom, max_zoom = 0.5, 3.0

    # Generate the binomial tree
    tree, price_tree = option_tree(stock_price, ex_price, uptick, downtick, risk_free_pct, time_steps, delta_time_step)

    # Variables for dragging functionality
    dragging = False
    offset_x, offset_y = 0, 0
    last_mouse_x, last_mouse_y = None, None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                dragging = True
                last_mouse_x, last_mouse_y = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    dx, dy = event.pos[0] - last_mouse_x, event.pos[1] - last_mouse_y
                    offset_x += dx
                    offset_y += dy
                    last_mouse_x, last_mouse_y = event.pos
            if event.type == pygame.MOUSEWHEEL:
                zoom += event.y * 0.1
                zoom = max(min_zoom, min(max_zoom, zoom))

        screen.fill((0, 0, 0))
        draw_tree(screen, tree, price_tree, height, time_steps, offset_x, offset_y, zoom)
        pygame.display.flip()

    pygame.quit()

# ------------------------------
# Main Execution
# ------------------------------

if __name__ == "__main__":
    visualize_binomial_tree(STOCK_PRICE, EX_PRICE, UPTICK, DOWNTICK, RISK_FREE_PCT, TIME_STEPS, DELTA_TIME_STEP)
