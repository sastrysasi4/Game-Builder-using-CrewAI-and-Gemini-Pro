
import pygame
import random

# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

# Set the height and width of the screen
size = [500, 700]
screen = pygame.display.set_mode(size)

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

# Speed in pixels per second
x_speed = 500.
y_speed = 500.

# Current position
x_coord = 100.
y_coord = 100.

# Create a ball
ball_width = 20
ball_height = 20
ball_x = random.randint(0, 480)
ball_y = 0

# Create a basket
basket_width = 100
basket_height = 20
basket_x = 200
basket_y = 600

# Store the number of balls caught
balls_caught = 0

# Store the number of balls dropped
balls_dropped = 0

# Speed up the ball after every 10 balls caught
speed_increase = 10

# Main game loop
while not done:
    # This limits the while loop to a max of 60 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(60)

    for event in pygame.event.get():   # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True   # Flag that we are done so we exit this loop

    # Clear the screen and set the screen background
    screen.fill(WHITE)

    # Move the ball
    ball_y += y_speed * clock.get_time() / 1000
    if ball_y > 600:
        ball_x = random.randint(0, 480)
        ball_y = 0
        balls_dropped += 1
        if balls_dropped == 3:
            done = True

    # Move the basket
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        basket_x -= x_speed * clock.get_time() / 1000
    if keys[pygame.K_RIGHT]:
        basket_x += x_speed * clock.get_time() / 1000

    # Check if the ball has hit the basket
    if ball_y + ball_height >= basket_y and ball_x >= basket_x and ball_x + ball_width <= basket_x + basket_width:
        balls_caught += 1
        balls_dropped = 0
        if balls_caught % speed_increase == 0:
            y_speed += 100

        # Move the ball to a random location
        ball_x = random.randint(0, 480)
        ball_y = 0

    # Draw the ball
    pygame.draw.rect(screen, BLUE, [ball_x, ball_y, ball_width, ball_height])

    # Draw the basket
    pygame.draw.rect(screen, RED, [basket_x, basket_y, basket_width, basket_height])

    # Display the number of balls caught
    font = pygame.font.SysFont('Calibri', 25, False, True)
    text = font.render("Balls Caught: " + str(balls_caught), True, BLACK)
    screen.blit(text, [10, 10])

    # Display the number of balls dropped
    font = pygame.font.SysFont('Calibri', 25, False, True)
    text = font.render("Balls Dropped: " + str(balls_dropped), True, BLACK)
    screen.blit(text, [10, 40])

    # Update the screen
    pygame.display.flip()

# End of game loop
pygame.quit()