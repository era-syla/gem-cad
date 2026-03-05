import cadquery as cq

# --- Parametric Dimensions (LEGO Standard) ---
# A LEGO unit (u) is 1.6mm
pitch = 8.0          # Distance between stud centers (5u)
stud_dia = 4.8       # Diameter of the stud (3u)
stud_height = 1.7    # Height of the stud (roughly 1u, usually 1.7 or 1.8mm)
wall_thickness = 1.2 # Standard wall thickness for shell (approx)
height = 9.6         # Standard brick height (6u)

# Dimensions for a 2x4 brick
width_units = 2
length_units = 4
width = width_units * pitch
length = length_units * pitch

# Tolerance (play) so bricks fit together
play = 0.1 # per side, usually 0.1mm gap total, so 0.2mm smaller overall
total_width = width - (2 * play)
total_length = length - (2 * play)

# Internal tube dimensions (for the bottom connection)
tube_outer_dia = 6.51 # (pitch * sqrt(2)) - stud_dia approximately
tube_inner_dia = 4.8  # Fits onto stud

# --- Modeling ---

# 1. Create the main rectangular body
brick = cq.Workplane("XY").box(total_length, total_width, height)

# 2. Add the studs on top
# We need to calculate the positions relative to the center
# The pitch grid is centered on the origin
x_coords = [(i * pitch) - (length / 2) + (pitch / 2) for i in range(length_units)]
y_coords = [(i * pitch) - (width / 2) + (pitch / 2) for i in range(width_units)]

# Generate a list of all stud (x, y) center points
stud_locations = [(x, y) for x in x_coords for y in y_coords]

brick = (
    brick.faces(">Z")
    .workplane()
    .pushPoints(stud_locations)
    .circle(stud_dia / 2)
    .extrude(stud_height)
)

# 3. Shelling the brick (hollowing out the bottom)
# We select the bottom face and shell inwards
brick = brick.faces("<Z").shell(-wall_thickness)

# 4. Add the internal tubes for structural integrity and clutch power
# For a 2x4 brick, there is a row of 3 tubes in the center gap between studs
# Tube locations are between the stud rows
if width_units > 1 and length_units > 1:
    tube_x_coords = [(i * pitch) - (length / 2) + pitch for i in range(length_units - 1)]
    tube_y_coords = [(i * pitch) - (width / 2) + pitch for i in range(width_units - 1)]
    
    tube_locations = [(x, y) for x in tube_x_coords for y in tube_y_coords]
    
    # We extrude the tubes from the inside ceiling down to the bottom
    # The shell operation leaves the "ceiling" at z = height/2 - wall_thickness
    # We want the tubes to go down to z = -height/2
    
    # Create the tubes
    tubes = (
        cq.Workplane("XY")
        .workplane(offset=(height / 2) - wall_thickness) # Start at inside ceiling
        .pushPoints(tube_locations)
        .circle(tube_outer_dia / 2)
        .circle(tube_inner_dia / 2)
        .extrude(-(height - wall_thickness)) # Extrude downwards
    )
    
    # Combine the brick shell with the tubes
    result = brick.union(tubes)
else:
    result = brick

# --- Visualization ---
# (If running in an environment that doesn't auto-display, result is stored here)