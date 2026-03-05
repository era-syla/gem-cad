import cadquery as cq

# LEGO-style 2x4 brick
# Standard LEGO dimensions
stud_diameter = 4.8
stud_height = 1.8
stud_spacing = 8.0
brick_width = 2 * stud_spacing   # 16mm (2 studs wide)
brick_length = 4 * stud_spacing  # 32mm (4 studs long)
brick_height = 19.2              # standard brick height

# Create main brick body
result = cq.Workplane("XY").box(brick_width, brick_length, brick_height)

# Add studs on top (2 columns x 4 rows)
# Stud positions centered on top face
stud_positions = []
for col in range(2):
    for row in range(4):
        x = -stud_spacing/2 + col * stud_spacing
        y = -1.5 * stud_spacing + row * stud_spacing
        stud_positions.append((x, y))

# Add each stud
for (sx, sy) in stud_positions:
    result = (
        result
        .faces(">Z")
        .workplane()
        .center(sx, sy)
        .circle(stud_diameter / 2)
        .extrude(stud_height)
    )