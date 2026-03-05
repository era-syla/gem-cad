import cadquery as cq

# Parametric dimensions
block_length = 100.0
block_width = 100.0
block_height = 40.0

boss_diameter = 15.0
boss_height = 5.0
hex_hole_width = 8.0  # Distance across flats
hex_hole_depth = 4.0

# Position of the boss relative to the center of the face
# Placing it in one corner as shown in the image
boss_offset_x = -block_length / 2.0 + 20.0
boss_offset_y = -block_width / 2.0 + 20.0

# Create the main block
base = cq.Workplane("XY").box(block_length, block_width, block_height)

# Create the boss with the hex hole
# We select the top face, move to the specific location, draw the boss circle and extrude it
# Then we draw the hex polygon and cut it
result = (
    base.faces(">Z")
    .workplane()
    .center(boss_offset_x, boss_offset_y)
    .circle(boss_diameter / 2.0)
    .extrude(boss_height)
    .faces(">Z")
    .workplane()
    .polygon(6, hex_hole_width / (3**0.5)) # Radius for circumscribed circle based on flat-to-flat distance
    .cutBlind(-hex_hole_depth)
)