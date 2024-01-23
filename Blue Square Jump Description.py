"""
Game Overview:

Title: Doodle Jump Clone
Genre: Arcade/Platformer
Platform: PC (Playable via Python with Pygame)
Creator: Jarett Spuck

Game Description:

This game is a vertical platformer where players control a character that constantly jumps upwards. The objective is to reach as high as possible without falling off the platforms or hitting obstacles. The game's challenge increases as the player ascends, with more difficult obstacles and platform patterns appearing.

Key Features:

1. Dynamic Camera Movement: The camera follows the player as they ascend. Platforms move downwards when the player reaches a certain height, keeping the player in view.
2. Procedurally Generated Platforms: Platforms are generated randomly in terms of position and type, ensuring a unique experience in each playthrough.
3. Increasing Difficulty: As the player progresses, the game becomes more challenging. This includes narrower platforms and the introduction of moving or falling platforms.
4. Power-Ups: The game features several power-ups to assist the player:
   - Super Jump (Pink Power-Up): Gives a moderate boost upwards.
   - Super Duper Jump (Purple Power-Up): Provides a significant vertical boost.
   - GOD Jump (Gold Power-Up): Offers an extremely high jump, allowing the player to bypass a large number of platforms.
5. Obstacles: Red triangle spikes serve as obstacles. Landing on these spikes ends the game, but passing through them from below is safe.
6. Score Tracking: The game keeps track of the player's score, which increases based on the number of platforms passed. The score is displayed on the screen during gameplay.
7. High Score: The game records the highest score achieved in a session, encouraging players to beat their personal bests.
8. Main Menu: Before gameplay, a main menu is presented with options to 'Start' the game, view 'How to Play' for instructions, or 'Quit.' The "How to Play" section provides a brief overview of the game mechanics and power-ups.

Gameplay Mechanics:

- Movement: The player uses keyboard inputs to move the character left or right.
- Jumping: The character automatically jumps continuously. Additional jumps can be triggered by pressing a key.
- Falling: If the player misses a platform and falls off the screen, the game ends.
- Collisions: The player must avoid spikes and use platforms to ascend further.

Technical Aspects:

- The game is built using Python and the Pygame library, making it easy to run on most computers with Python installed.
- Graphics are simple, utilizing basic shapes and colors for clarity and ease of understanding.

Conclusion:

This Doodle Jump Clone offers a fun and challenging experience, suitable for quick play sessions. Its randomly generated platforms and increasing difficulty provide a fresh and engaging experience each time. The inclusion of power-ups and a high score system adds to the replay value, encouraging players to improve their skills and reach new heights.
"""
