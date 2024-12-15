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
GAME_SPEED = 10
BOAT_SPEED = 1
DRONE_SPEED = 2
SCREEN_RADIUS = 20
NUM_DRONES = 1
DETECTION_INTERVAL = 5
SONAR_RANGE = 25 #TODO

#Submarine setting
SUBMARINE_SPEED = 1.6
TORPEDO_RANGE = 26.2
SUB_SONAR_RANGE = 100

# Plotting
submarine_detected_count = 0  # Count games ending with submarine detection
torpedo_range_count = 0      # Count games ending with boat in torpedo range
game_count = 0
frame_count = 0
game_distances = []  # List to store distances per game

class Boat:
    def __init__(self):
        self.x, self.y = self.random_edge_point()
        self.target_x, self.target_y = self.random_edge_point()
        self.speed = BOAT_SPEED
        self.size = 5
        self.heading = 0  # In degrees, 0 means pointing right

    def random_edge_point(self):
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
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < self.speed:
            self.x, self.y = self.target_x, self.target_y
            self.target_x, self.target_y = self.random_edge_point()
        else:
            self.x += self.speed * (dx / distance)
            self.y += self.speed * (dy / distance)

        # Calculate heading based on movement direction
        self.heading = math.degrees(math.atan2(dy, dx))  # Angle in degrees

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.size)


class Drone:
    def __init__(self, start_angle, end_angle, radius):
        self.start_angle = start_angle  # The minimum angle the drone oscillates to
        self.end_angle = end_angle      # The maximum angle the drone oscillates to
        self.current_angle = start_angle  # The current angle of the drone
        self.radius = radius
        self.transition_speed = 3.5  # Speed of angle change (degrees per frame)
        self.moving_to_end = True  # Whether the drone is moving towards the end_angle
        self.detecting = False
        self.size = 2
        self.last_detection_frame = 0
        self.x = 0
        self.y = 0

    def detect(self, frame_count):
        self.detecting = False
        if frame_count - self.last_detection_frame >= DETECTION_INTERVAL:
            self.last_detection_frame = frame_count
            self.detecting = True

    def update_angle(self):
        """Oscillate between start_angle and end_angle."""
        if self.moving_to_end:
            self.current_angle += self.transition_speed
            if self.current_angle >= self.end_angle:  # Check if it reaches the upper limit
                self.current_angle = self.end_angle  # Snap to the end angle
                self.moving_to_end = False  # Reverse direction
        else:
            self.current_angle -= self.transition_speed
            if self.current_angle <= self.start_angle:  # Check if it reaches the lower limit
                self.current_angle = self.start_angle  # Snap to the start angle
                self.moving_to_end = True  # Reverse direction

    def move(self, boat_x, boat_y, boat_heading):
        # Update the current angle based on oscillation
        self.update_angle()

        # Calculate the position relative to the boat's heading
        relative_angle = boat_heading + self.current_angle
        angle = math.radians(relative_angle % 360)  # Ensure angle is within 0-360 degrees
        self.x = boat_x + self.radius * math.cos(angle)
        self.y = boat_y + self.radius * math.sin(angle)

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), self.size)
        if self.detecting:
            pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), SONAR_RANGE, 1)




class Submarine:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.detected = False
        self.size = 5
        self.speed = SUBMARINE_SPEED

    def move_towards_boat(self, boat, trigger_distance):
        """Move towards the boat if within the trigger distance."""
        # Calculate the distance to the boat
        dx = boat.x - self.x
        dy = boat.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance <= trigger_distance:
            # Normalize the direction and move towards the boat
            if distance > 0:
                self.x += self.speed * (dx / distance)
                self.y += self.speed * (dy / distance)

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


def calculate_heading(boat):
    """Calculate the normalized direction vector of the boat."""
    dx = boat.target_x - boat.x
    dy = boat.target_y - boat.y
    distance = math.sqrt(dx**2 + dy**2)
    if distance == 0:
        return 0, 0  # Avoid division by zero if the boat is stationary
    return dx / distance, dy / distance


# Heatmap grid settings
HEATMAP_GRID_SIZE = 1  # Size of each grid cell
GRID_WIDTH = WIDTH // HEATMAP_GRID_SIZE
GRID_HEIGHT = HEIGHT // HEATMAP_GRID_SIZE

# Initialize the heatmap
heatmap = np.zeros((GRID_HEIGHT, GRID_WIDTH))

def update_heatmap(boat, submarine):
    """Update heatmap with the submarine's position relative to the boat's heading."""
    # Calculate the relative position of the submarine
    rel_x = submarine.x - boat.x
    rel_y = submarine.y - boat.y

    # Rotate the relative position to align with the boat's heading
    heading_rad = math.radians(boat.heading - 90)  # Convert heading to radians
    rotated_x = rel_x * math.cos(-heading_rad) - rel_y * math.sin(-heading_rad)
    rotated_y = rel_x * math.sin(-heading_rad) + rel_y * math.cos(-heading_rad)

    # Convert rotated position to grid coordinates
    grid_x = int((rotated_x + WIDTH // 2) // HEATMAP_GRID_SIZE)
    grid_y = int((rotated_y + HEIGHT // 2) // HEATMAP_GRID_SIZE)

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

    # Add the torpedo range overlay
    circle = plt.Circle((0, 0), radius=TORPEDO_RANGE, color='blue', fill=False, linestyle='--', label='Torpedo Range')
    plt.gca().add_artist(circle)
    plt.colorbar(label="Frequency")
    plt.grid(False)
    plt.show()

def display_distance_chart():
    """Display a line chart of distances between the boat and submarine for each game."""
    global game_distances

    # Calculate the average distance
    average_distance = sum(game_distances) / len(game_distances)

    # Plot the distances
    plt.figure(figsize=(10, 6))
    plt.title("Boat-Submarine Distances per Game")
    plt.xlabel("Game Number")
    plt.ylabel("Distance")
    plt.plot(range(1, len(game_distances) + 1), game_distances, label="Distance per Game")
    plt.axhline(average_distance, color='red', linestyle='--', label=f"Average Distance ({average_distance:.2f})")
    plt.legend()
    plt.grid(True)
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

def reset_game():
    global boat, drones, submarine, frame_count, game_count

    # Calculate distance between boat and submarine
    if game_count > 0:  # Skip first reset since no distance exists yet
        boat_submarine_distance = math.sqrt(
            (boat.x - submarine.x) ** 2 + (boat.y - submarine.y) ** 2
        )
        game_distances.append(boat_submarine_distance)  # Record the distance

    boat = Boat()
    if game_count >= 1000:
        print('1000 games completed')
        display_distance_chart()  # Show the distance chart
        display_heatmap()
        display_pie_chart()
        pygame.quit()
        sys.exit()

    drones = [
        Drone(start_angle=-0, end_angle=0, radius=SCREEN_RADIUS)
        for _ in range(NUM_DRONES)
    ]

    submarine_x, submarine_y = place_submarine_away_from_boat(boat, 70)
    submarine = Submarine(submarine_x, submarine_y)
    frame_count = 0
    game_count += 1


# Initializing game
reset_game()

# Main game loop
running = True
TRIGGER_DISTANCE = 100  # Distance at which the submarine starts moving toward the boat

while running:
    screen.fill(WHITE)
    frame_count += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the boat
    boat.move_to_target()

    # Move the submarine toward the boat if within the trigger distance
    submarine.move_towards_boat(boat, TRIGGER_DISTANCE)

    # Calculate the boat's heading
    heading_x, heading_y = calculate_heading(boat)

    boat_submarine_distance = math.sqrt((boat.x - submarine.x) ** 2 + (boat.y - submarine.y) ** 2)

    # Update drones to stay in an arc at the screen radius, avoiding the excluded area
    for drone in drones:
        drone.move(boat.x, boat.y, boat.heading)

    # Check for submarine detection and other logic
    submarine_detected = False
    for drone in drones:
        drone.detect(frame_count)

        # Calculate distance to the submarine
        dist = math.sqrt((drone.x - submarine.x) ** 2 + (drone.y - submarine.y) ** 2)
        if dist <= SONAR_RANGE and drone.detecting:
            submarine_detected = True

    if boat_submarine_distance <= TORPEDO_RANGE:
        print("Boat entered torpedo range! Resetting game...")
        torpedo_range_count += 1  # Increment torpedo range counter
        update_heatmap(boat, submarine)  # Capture the last frame's data
        reset_game()
        continue

    if submarine_detected:
        print("Submarine detected! Resetting game...")
        submarine_detected_count += 1
        update_heatmap(boat, submarine)
        reset_game()
        continue

    # Draw everything
    boat.draw(screen)
    for drone in drones:
        drone.draw(screen)
    submarine.draw(screen)

    pygame.display.flip()
    clock.tick(GAME_SPEED)


pygame.quit()