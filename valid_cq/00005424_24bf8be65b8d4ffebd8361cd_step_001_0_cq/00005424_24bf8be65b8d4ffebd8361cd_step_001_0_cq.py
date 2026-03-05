import cadquery as cq

# --- Parameter Definitions ---
cube_size = 10.0
text_size = 6.0
text_thickness = 1.0  # Height of the text extrusion
text_font = "Arial"   # Standard font
spacing_x = 25.0      # Horizontal spacing between cube centers
spacing_y = 25.0      # Vertical spacing between cube centers

# --- Helper Function ---
def make_numbered_cube(number, x_pos, y_pos):
    """
    Creates a cube with a number extruded on top at a specific position.
    """
    # Create the base cube
    # Centered on Z to make placement easier, but we'll move it up so Z=0 is bottom
    cube = cq.Workplane("XY").box(cube_size, cube_size, cube_size)
    
    # Create the text
    # We select the top face (Z-positive) to place the text on
    text_geo = (
        cube.faces(">Z").workplane()
        .text(str(number), fontsize=text_size, distance=text_thickness, font=text_font)
    )
    
    # Move the entire assembly to the desired X, Y location
    final_obj = text_geo.translate((x_pos, y_pos, 0))
    return final_obj

# --- Layout Configuration ---
# The image shows a diamond/rhombus pattern.
# Let's map positions based on a grid but select only specific points.
# A standard numeric keypad layout is often:
# 7 8 9
# 4 5 6
# 1 2 3
# But looking closely at the image:
# Top: 7? (looks like <)
# Top-Left: 8
# Top-Right: 4
# Far-Left: 6
# Center: 5
# Far-Right: 1
# Bottom-Left: 9
# Bottom-Right: 2
# Bottom: 3
#
# Let's re-examine the image orientation.
# It looks rotated.
# If we rotate the image 45 degrees clockwise mentally:
#   7
# 8   4
#   5
# 6   2
#   9
#     3
#
# Wait, let's look at the numbers themselves.
# The center is clearly '5'.
# To the right of 5 is '1' (or 'L'?). No, it's '1'.
# To the left of 5 is '6' (or '9' upside down). Let's assume '6'.
# Above 5 is '7' (looks like an upside down L).
# Below 5 is '3'.
# Top Left of center is '8'.
# Top Right of center is '4'.
# Bottom Left of center is '9'.
# Bottom Right of center is '2'.
#
# This corresponds to a rotated 3x3 grid:
#      7
#    8   4
#  6   5   1
#    9   2
#      3
#
# Wait, that's not quite a standard keypad.
# Let's trace coordinates relative to center (0,0) for '5'.
#
# Center (0,0): 5
#
# Top (0, +2*spacing): 7
# Bottom (0, -2*spacing): 3
# Left (-2*spacing, 0): 6
# Right (+2*spacing, 0): 1
#
# Top-Left (-spacing, +spacing): 8
# Top-Right (+spacing, +spacing): 4
# Bottom-Left (-spacing, -spacing): 9
# Bottom-Right (+spacing, -spacing): 2
#
# This layout puts 6,5,1 on the X-axis and 7,5,3 on the Y-axis?
# Let's check the image again.
# The image shows a diamond shape.
# Top point: 7? It looks like a 'V' or 'L'. It's likely a '7' rotated.
# Far Right point: 1.
# Far Left point: 6.
# Bottom point: 3.
# The inner square around 5 consists of 8, 4, 2, 9.
#
# Let's verify the "inner square" logic.
# Between 6 and 7 is 8.
# Between 7 and 1 is 4.
# Between 1 and 3 is 2.
# Between 3 and 6 is 9.
#
# Coordinate mapping (assuming diamond grid):
# Center: (0,0) -> 5
#
# Ring 1 (Inner):
# (-x, +y) -> 8
# (+x, +y) -> 4
# (+x, -y) -> 2
# (-x, -y) -> 9
#
# Ring 2 (Outer points):
# (0, +2y) -> 7  (Top)
# (+2x, 0) -> 1  (Right)
# (0, -2y) -> 3  (Bottom)
# (-2x, 0) -> 6  (Left)
#
# Note on rotation: The numbers in the image are oriented relative to the global coordinates,
# not rotated with the grid. For example, the '5' is upright.
#
# Let's define offsets.
dx = spacing_x
dy = spacing_y

# Dictionary mapping number to (x, y) coordinates
positions = {
    5: (0, 0),
    8: (-dx, dy),
    4: (dx, dy),
    2: (dx, -dy),
    9: (-dx, -dy),
    7: (0, 2 * dy),
    1: (2 * dx, 0),
    3: (0, -2 * dy),
    6: (-2 * dx, 0)
}

# --- Geometry Generation ---

# Container for all cubes
result = cq.Workplane("XY")

# Iterate through the definitions and union them
first = True
for num, (x, y) in positions.items():
    part = make_numbered_cube(num, x, y)
    if first:
        result = part
        first = False
    else:
        result = result.union(part)

# Export or visualization handling (standard CadQuery practice is simply defining 'result')