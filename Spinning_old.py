import pygame
import sys
import random
import math
import numpy as np
import matplotlib.pyplot as plt

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drone Detection")
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Simulation settings
GAME_SPEED = 9999999
BOAT_SPEED = 1
DRONE_SPEED = 2
NUM_DRONES = 1
SCREEN_RADIUS = 20
DETECTION_INTERVAL = 6
SONAR_RANGE = 25 #TODO

#Submarine setting
SUBMARINE_SPEED = 0
TORPEDO_RANGE = 20 * 1.852
SUB_SONAR_RANGE = 100

# Plotting
submarine_detected_count = 0  # Count games ending with submarine detection
torpedo_range_count = 0      # Count games ending with boat in torpedo range
game_count = 0
frame_count = 0

class Boat:
    def __init__(self):
        self.x, self.y = self.random_edge_point()
        self.target_x, self.target_y = self.random_edge_point()
        self.speed = BOAT_SPEED
        self.size = 5

    def random_edge_point(self):
        """Generate a random point on the screen's edges."""
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            return random.randint(0, WIDTH), 0
        elif edge == 'bottom':
            return random.randint(0, WIDTH), HEIGHT
        elif edge == 'left':
            return 0, random.randint(0, HEIGHT)
        elif edge == 'right':
            return WIDTH, random.randint(0, HEIGHT)

    def move_to_target(self):
        """Move smoothly towards the target point."""
        # Calculate the distance and direction to the target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        # If we're close enough to the target, pick a new target
        if distance < self.speed:
            self.x, self.y = self.target_x, self.target_y
            self.target_x, self.target_y = self.random_edge_point()
        else:
            # Normalize direction and move towards the target
            self.x += self.speed * (dx / distance)
            self.y += self.speed * (dy / distance)


    def draw(self, screen):
        pygame.draw.circle(screen, BLUE,  (self.x, self.y), self.size, self.size)

class Drone:
    def __init__(self, angle, radius):
        self.angle = angle
        self.radius = radius
        self.detecting = False
        self.size = 2
        self.last_detection_frame = 0
        self.x = 0
        self.y = 0
        self.angular_speed = 0.2 #DRONE_SPEED / radius  # Angular speed linked to drone speed


    def detect(self, frame_count):
        # Reset detecting to False at the start of the frame
        self.detecting = False

        # Check if enough frames have passed since last detection
        if frame_count - self.last_detection_frame >= DETECTION_INTERVAL:
            self.last_detection_frame = frame_count  # Update last detection frame
            self.detecting = True


    def move(self, boat_x, boat_y):
        # Increment the angle based on the angular speed
        self.angle += self.angular_speed
        # Calculate the new position based on the boat's position
        self.x = boat_x + SCREEN_RADIUS * math.cos(self.angle)
        self.y = boat_y + SCREEN_RADIUS * math.sin(self.angle)

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), self.size)
        if self.detecting:
            pygame.draw.circle(screen, GREEN, (self.x, self.y), SONAR_RANGE, 1)

class Submarine:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.detected = False
        self.size = 5

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), SUB_SONAR_RANGE, 1)
        pygame.draw.circle(screen, RED, (self.x, self.y), TORPEDO_RANGE, 1)
        if self.detected:
            pygame.draw.circle(screen, RED, (self.x, self.y), self.size)
        else:
            pygame.draw.circle(screen, RED, (self.x, self.y), self.size, 3)

# Helper functions
def place_submarine_away_from_boat(boat, min_distance):
    while True:
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        dist = math.sqrt((x - boat.x)**2 + (y - boat.y)**2)
        if dist > min_distance:
            return x, y


# Heatmap grid settings
HEATMAP_GRID_SIZE = 1  # Size of each grid cell
GRID_WIDTH = WIDTH // HEATMAP_GRID_SIZE
GRID_HEIGHT = HEIGHT // HEATMAP_GRID_SIZE

# Initialize the heatmap
heatmap = np.zeros((GRID_HEIGHT, GRID_WIDTH))

def update_heatmap(boat, submarine):
    """Update heatmap with the submarine's position relative to the boat."""
    rel_x = submarine.x - boat.x
    rel_y = submarine.y - boat.y

    # Convert relative position to grid coordinates
    grid_x = int((rel_x + WIDTH // 2) // HEATMAP_GRID_SIZE)
    grid_y = int((rel_y + HEIGHT // 2) // HEATMAP_GRID_SIZE)

    # Ensure grid coordinates are within bounds
    if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
        heatmap[grid_y][grid_x] += 1

def display_heatmap():
    """Display the heatmap in a separate Matplotlib window."""
    plt.figure(figsize=(8, 6))
    plt.title("Heatmap of Submarine Positions Relative to Boat")
    plt.xlabel("Relative X Position (Grid)")
    plt.ylabel("Relative Y Position (Grid)")

    max_value = np.max(heatmap)
    if max_value > 0:
        normalized_heatmap = (heatmap / max_value * 255).astype(int)
    else:
        normalized_heatmap = heatmap

    plt.imshow(
        normalized_heatmap,
        extent=[-WIDTH // 2, WIDTH // 2, -HEIGHT // 2, HEIGHT // 2],
        origin="lower",
        cmap="hot",
        interpolation="nearest"
    )
    circle = plt.Circle((0, 0), radius=TORPEDO_RANGE, color='blue', fill=False, linestyle='--', label='Torpedo Range')
    plt.gca().add_artist(circle)
    plt.colorbar(label="Frequency")
    plt.grid(False)
    plt.show()

def display_pie_chart():
    """Display a pie chart of game-ending conditions."""
    labels = ['Submarine Detected', 'Boat in Torpedo Range']
    sizes = [submarine_detected_count, torpedo_range_count]
    colors = ['lightblue', 'salmon']
    explode = (0.1, 0)  # Slightly explode the first slice for emphasis

    plt.figure("Game Outcomes", figsize=(6, 6))
    plt.title("Proportions of Game-Ending Conditions (1000 Games)")
    plt.pie(
        sizes, labels=labels, autopct='%1.1f%%', startangle=140,
        colors=colors, explode=explode, shadow=True
    )
    plt.show()

# Reset function
def reset_game():
    """Reset all game objects to their initial state."""
    global boat, drones, submarine, frame_count, game_count
    # Reset boat
    boat = Boat()

    if game_count >= 1000:
        print('1000 games completed')
        display_heatmap()
        display_pie_chart()  # Display the pie chart
        pygame.quit()  # Exit the game after displaying the heatmap
        sys.exit()


    # Reset drones
    drones = [
        Drone(angle=2.0 * math.pi * i / NUM_DRONES, radius=SCREEN_RADIUS)
        for i in range(NUM_DRONES)
    ]

    # Reset submarine
    submarine_x, submarine_y = place_submarine_away_from_boat(boat, 70)
    submarine = Submarine(submarine_x, submarine_y)

    # Reset frame counter
    frame_count = 0

    game_count += 1


# Initializing game
reset_game()

# Main game loop
running = True
while running:
    screen.fill(WHITE)
    frame_count += 1


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    boat.move_to_target()

    boat_submarine_distance = math.sqrt((boat.x - submarine.x) ** 2 + (boat.y - submarine.y) ** 2)
    if boat_submarine_distance <= TORPEDO_RANGE:
        print("Boat entered torpedo range! Resetting game...")
        torpedo_range_count += 1  # Increment torpedo range counter
        update_heatmap(boat, submarine)  # Capture the last frame's data
        reset_game()
        continue

    # Update drones and check if submarine is detected
    submarine_detected = False  # Track if any drone detects the submarine
    for drone in drones:
        drone.move(boat.x, boat.y)

        # Check detection for each drone
        drone.detect(frame_count)

        # Calculate the distance between the drone and the submarine
        dist = math.sqrt((drone.x - submarine.x) ** 2 + (drone.y - submarine.y) ** 2)

        # Check if the submarine is within sonar range
        if dist <= SONAR_RANGE and drone.detecting:
            submarine.detected = True  # Update the submarine's state
        else:
            submarine.detected = False  # Reset detection if not in range
        # Check if submarine is detected
        if submarine.detected:
            print("Submarine detected! Resetting game...")
            submarine_detected_count += 1  # Increment submarine detection counter
            update_heatmap(boat, submarine)  # Capture the last frame's data
            reset_game()
            continue

    # Draw everything
    boat.draw(screen)
    for drone in drones:
        drone.draw(screen)
    submarine.draw(screen)  # Uncomment to debug



    #pygame.display.flip()
    clock.tick(GAME_SPEED)

pygame.quit()