from ursina import *  # Importing Ursina library
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

app = Ursina()

# Set the default shader
Entity.default_shader = lit_with_shadows_shader

# Create the player
player = FirstPersonController(collider='box', speed=6.5)
player.cursor.visible = False

# Create the ground
ground = Entity(
    model='plane',
    texture='white_cube',
    collider='mesh',
    scale=(30, 0.1, 10),
    color=color.gray,
)

# Create red lines (chiziq)
chiziq_positions = [-0.7, -3.7, 3.7]  # Removed 8.6 position
chiziqs = [
    Entity(
        model='cube',
        color=color.red,
        scale=(0.4, 0.1, 50),
        z=25,
        x=pos
    )
    for pos in chiziq_positions
]

# Create blocks closer together
blocks = []
sky = Sky(color=color.cyan)

for i in range(20):
    is_correct = bool(i % 2)  # Alternate between True and False for is_correct

    block1 = Entity(
        model='cube',
        collider='box',
        color=color.azure,
        position=(2, 0.3, 2 + i * 3),  # Adjusted z-spacing
        scale=(3, 0.1, 2.5),
        texture='glass',  # Adding a glass texture
    )
    block2 = Entity(
        model='cube',
        collider='box',
        color=color.azure,
        position=(-2, 0.3, 2 + i * 3),  # Adjusted z-spacing
        scale=(3, 0.1, 2.5),
        texture='glass',  # Adding a glass texture
    )
    blocks.append((block1, block2, is_correct))

# Create the goal
goal = Entity(
    color=color.gold,
    model='cube',
    z=62,  # Adjusted position to match closer blocks
    collider='box',
    scale=(10, 1, 20),
)

# Define the update function
def update():
    for block1, block2, is_correct in blocks:
        for x, correct in [(block1, is_correct), (block2, not is_correct)]:
            if x.intersects() and not correct:
                invoke(destroy, x, delay=0.2)
                x.fade_out(duration=0.2)

    # Reset player position if they fall off
    if player.y < -50:
        player.y = 2
        player.z = 0
        player.x = 0

    # Check if player reaches the goal
    if player.intersects(goal).hit:
        player.speed = 0
        Text(
            text='You Win!',
            color=color.red,
            scale=2,
            origin=(0, 0),
            position=(0, 0.4),
            background=True
        )

# Add lighting
sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1))
AmbientLight(color=color.rgba(255, 255, 255, 0.2))  # Ambient light for better visibility

app.run()
