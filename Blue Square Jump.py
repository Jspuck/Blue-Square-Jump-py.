import pygame
import random

# Initialize Pygame and Font module
pygame.init()
pygame.font.init()

# Game Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
PLAYER_SIZE = 50
PLATFORM_WIDTH, PLATFORM_HEIGHT = 70, 20
CIRCLE_RADIUS = 25  # Radius for circle platforms
TRIANGLE_SIZE = 20  # Size of the triangle obstacles
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 20, 20  # Size of the obstacles
FULL_PLATFORM_WIDTH = SCREEN_WIDTH
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)  # Color for the obstacles and triangles
GREEN = (0, 255, 0)  # Color for circle platforms
GOLD = (255, 215, 0)  # Color for the Super Jump Power-Up
PURPLE = (128, 0, 128)  # Color for the Super Duper Jump Power-Up
PINK = (255, 105, 180)  # Color for the GOD Jump Power-Up
GRAVITY = 0.5
MAX_JUMP_HEIGHT = 15
SUPER_JUMP_HEIGHT = 30  # Height for the super jump
SUPER_DUPER_JUMP_HEIGHT = 2 * SUPER_JUMP_HEIGHT  # Double the height of the super jump
CAMERA_FOLLOW_HEIGHT = SCREEN_HEIGHT // 2
PLATFORM_DISTANCE = 100  # Vertical distance between platforms
STARTING_PLATFORM_Y = SCREEN_HEIGHT - 50  # Starting Y position for the platform
FPS = 60
PLATFORMS_PASSED_THRESHOLD = 25  # Threshold for increased difficulty
CIRCLE_PLATFORMS_THRESHOLD = 50  # Threshold for circle platforms
FALLING_PLATFORM_THRESHOLD = 100  # Threshold for falling platforms
POWER_UP_FREQUENCY = 100  # Frequency of power-up platforms
SUPER_DUPER_JUMP_FREQUENCY = 20  # Frequency of super duper jump power-up

def show_menu(screen):
    menu_font = pygame.font.SysFont(None, 36)
    menu_options = ['Start', 'How to Play', 'Quit']
    selected_option = 0

    while True:
        screen.fill((0, 0, 0))  # Clear the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    return menu_options[selected_option]

        for i, option in enumerate(menu_options):
            color = WHITE if i == selected_option else (100, 100, 100)
            label = menu_font.render(option, True, color)
            screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 200 + i * 50))

        pygame.display.update()

def show_instructions(screen):
    instructions_font = pygame.font.SysFont(None, 28)
    instructions = [
        "Welcome to the game!",
        "It starts off easy and gets",
        "gets harder as you go up",
        "Sometimes you need to",
        "wait for blocks to fall",
        "to continue in some cases.",
        "Power-ups:",
        " - Gold: = GOD jump boost",
        " - Purple: Big boost",
        " - Pink: Small boost",
        "WARNING!",
        "Watch out for red spike traps!",
        "The small red squares are",
        "there to scare you,",
        "meaning it's safe to",
        "land on them.",
        "Press any key to go back."
    ]

    while True:
        screen.fill((0, 0, 0))  # Clear the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                return

        for i, line in enumerate(instructions):
            label = instructions_font.render(line, True, WHITE)
            screen.blit(label, (50, 50 + i * 30))

        pygame.display.update()

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blue Square Jump")

# Player Class
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = STARTING_PLATFORM_Y - PLAYER_SIZE
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.velocity = 10
        self.is_jumping = False
        self.jump_charge = 0
        self.fall_speed = 0
        self.jump_count = 0

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

    def move(self, direction):
        if direction == 'left' and self.x > 0:
            self.x -= self.velocity
        if direction == 'right' and self.x < SCREEN_WIDTH - self.width:
            self.x += self.velocity

    def start_jump(self):
        if self.jump_count < 2:
            self.is_jumping = True
            self.jump_charge = MAX_JUMP_HEIGHT
            self.jump_count += 1

    def update(self, platforms):
        if self.is_jumping:
            self.y -= self.jump_charge
            self.jump_charge -= 1
            if self.jump_charge <= 0:
                self.is_jumping = False
                self.fall_speed = 0
        else:
            self.y += self.fall_speed + GRAVITY
            self.fall_speed += GRAVITY

        # Move platforms down if player is above the camera follow height
        if self.y < CAMERA_FOLLOW_HEIGHT:
            diff = CAMERA_FOLLOW_HEIGHT - self.y
            self.y = CAMERA_FOLLOW_HEIGHT
            for platform in platforms:
                platform.y += diff

        # Check for landing on platforms
        for platform in platforms:
            if not self.is_jumping and self.fall_speed > 0:
                if (self.y + self.height >= platform.y) and (self.y < platform.y) and (self.x + self.width > platform.x) and (self.x < platform.x + platform.width):
                    self.y = platform.y - self.height
                    self.fall_speed = 0
                    self.jump_count = 0

                    # Check for landing on a spike
                    if platform.has_triangle:
                        return False  # End the game if landed on a spike

                    # Handle power-ups
                    if platform.has_power_up:
                        self.is_jumping = True
                        self.jump_charge = SUPER_JUMP_HEIGHT
                    elif platform.has_super_duper_power_up:
                        self.is_jumping = True
                        self.jump_charge = SUPER_DUPER_JUMP_HEIGHT
                    elif platform.has_god_jump:
                        self.is_jumping = True
                        self.jump_charge = 10 * MAX_JUMP_HEIGHT  # Adjusted jump charge for GOD jump

        if self.y > SCREEN_HEIGHT:
            return False
        return True

# Platform Class
class Platform:
    def __init__(self, x, y, width=PLATFORM_WIDTH, has_obstacle=False, is_circle=False, has_triangle=False, is_falling=False, has_power_up=False, has_super_duper_power_up=False, has_god_jump=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = PLATFORM_HEIGHT
        self.obstacle = has_obstacle
        self.is_circle = is_circle
        self.has_triangle = has_triangle
        self.is_falling = is_falling
        self.has_power_up = has_power_up
        self.has_super_duper_power_up = has_super_duper_power_up
        self.has_god_jump = has_god_jump
        self.time_player_on = 0  # Initialize this attribute
        self.passed_by_player = False  # New attribute to track if the player has passed this platform
        


    def draw(self):
        if self.is_circle:
            pygame.draw.circle(screen, GREEN, (self.x, self.y - CIRCLE_RADIUS), CIRCLE_RADIUS)
        else:
            pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
            if self.obstacle:
                pygame.draw.rect(screen, RED, (self.x + self.width // 2 - OBSTACLE_WIDTH // 2, self.y - OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
            if self.has_triangle:
                pygame.draw.polygon(screen, RED, [(self.x + self.width // 2, self.y - TRIANGLE_SIZE), (self.x + self.width // 2 - TRIANGLE_SIZE // 2, self.y), (self.x + self.width // 2 + TRIANGLE_SIZE // 2, self.y)])
        if self.has_power_up:
            pygame.draw.circle(screen, PINK, (self.x + self.width // 2, self.y - 30), 15)
        if self.has_super_duper_power_up:
            pygame.draw.circle(screen, PURPLE, (self.x + self.width // 2, self.y - 30), 15)
        if self.has_god_jump:
            pygame.draw.circle(screen, GOLD, (self.x + self.width // 2, self.y - 30), 15)  # Draw GOD jump power-up in pink
        

# Function to add new platform at the top
def add_new_platform(platforms, platforms_passed):
    if platforms:  # Check if the list is not empty
        new_platform_y = platforms[-1].y - PLATFORM_DISTANCE
    else:
        new_platform_y = STARTING_PLATFORM_Y - PLATFORM_DISTANCE

    new_platform_x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
    new_platform_width = PLATFORM_WIDTH
    is_circle = False
    has_obstacle = False
    has_triangle = False
    is_falling = False
    has_power_up = False
    has_super_duper_power_up = False
    has_god_jump = False

    if platforms_passed > PLATFORMS_PASSED_THRESHOLD:
        new_platform_width = max(PLATFORM_WIDTH - (platforms_passed - PLATFORMS_PASSED_THRESHOLD) * 2, 30)
        has_obstacle = random.choice([True, False]) and random.random() < 0.3

    if platforms_passed > CIRCLE_PLATFORMS_THRESHOLD:
        is_circle = random.choice([True, False])

    if platforms_passed > FALLING_PLATFORM_THRESHOLD:
        has_triangle = random.choice([True, False])
        is_falling = random.choice([True, False])

    # Add the Super Jump Power-Up (pink) approximately every 30 platforms
    if platforms_passed % 30 == 0 and platforms_passed != 0:
        has_power_up = True

    # Add the GOD Jump Power-Up (gold) every 70 platforms
    if platforms_passed % 70 == 0 and platforms_passed != 0:
        has_god_jump = True    

    if random.randint(0, SUPER_DUPER_JUMP_FREQUENCY - 1) == 0:
        has_super_duper_power_up = True

    platforms.append(Platform(new_platform_x, new_platform_y, new_platform_width, has_obstacle, is_circle, has_triangle, is_falling, has_power_up, has_super_duper_power_up, has_god_jump))




# Initialize Player and Platforms
player = Player()
platforms = [Platform(random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH), y) for y in range(STARTING_PLATFORM_Y, -600, -PLATFORM_DISTANCE)]
starting_platform = Platform(0, STARTING_PLATFORM_Y, FULL_PLATFORM_WIDTH)
platforms.append(starting_platform)
platforms_passed = 0

# Call the menu before entering the game loop
user_choice = show_menu(screen)
if user_choice == 'Start':
    # Proceed to game loop
    pass
elif user_choice == 'How to Play':
    show_instructions(screen)
    user_choice = show_menu(screen)  # Show the menu again after instructions
elif user_choice == 'Quit' or user_choice is None:
    pygame.quit()
    exit()

# Score Initialization
score = 0

# Game Loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))  # Clear the screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player Movement and Jump
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move('left')
    if keys[pygame.K_RIGHT]:
        player.move('right')
    if keys[pygame.K_SPACE] and not player.is_jumping and player.jump_count < 2:
        player.start_jump()

     # Update Player
    if not player.update(platforms):
        print(f"Game Over! Final Score: {score}")
        break

    # Check for platform pass and update score
    for platform in platforms:
        if (player.y + player.height < platform.y) and not platform.passed_by_player:
            score += 10
            platform.passed_by_player = True  # Mark this platform as passed

    # Reset the passed flag for platforms that are no longer relevant
    for platform in platforms:
        if platform.y > SCREEN_HEIGHT or (player.y + player.height >= platform.y and player.x + player.width > platform.x and player.x < platform.x + platform.width):
            platform.passed_by_player = False

    # Display Score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


    # Check for collisions with platforms and obstacles
    for platform in platforms:
        if player.y + player.height < platform.y and not platform.obstacle and not platform.is_circle and not platform.has_triangle:
            platforms_passed += 1
            break  # Increment once per platform and break

    # Update platforms_passed and falling platforms
    for platform in platforms:
        if platform.is_falling:
            if player.y + player.height >= platform.y and player.x + player.width > platform.x and player.x < platform.x + platform.width:
                platform.time_player_on += clock.get_time() / 1000  # Increment timer
                if platform.time_player_on > 0.5:
                    platform.y += 5  # Make the platform fall
            else:
                platform.time_player_on = 0  # Reset timer if player is not on the platform

    # Remove platforms that have moved off the screen and add new ones
    platforms = [platform for platform in platforms if platform.y < SCREEN_HEIGHT]
    if len(platforms) < 6 or platforms[-1].y < SCREEN_HEIGHT - PLATFORM_DISTANCE:
        add_new_platform(platforms, platforms_passed)

    # Draw Player and Platforms
    player.draw()
    for platform in platforms:
        platform.draw()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()