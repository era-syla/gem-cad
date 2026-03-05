import cadquery as cq

# Parametric dimensions
length = 140.0        # Total length of the base and wall
width = 60.0          # Width (depth) of the base plate
base_thickness = 8.0  # Thickness of the base plate
wall_height = 60.0    # Height of the vertical wall
wall_thickness = 6.0  # Thickness of the main vertical web
flange_depth = 18.0   # Depth of the end flanges (returns)
hole_diameter = 5.0   # Diameter of the 4 mounting holes
hole_margin_x = 10.0  # Distance of holes from side edges
hole_margin_z = 10.0  # Distance of holes from top/bottom edges

# 1. Create the base plate
# Centered at the origin
base = cq.Workplane("XY").box(length, width, base_thickness)

# 2. Create the vertical wall with C-channel profile
# We sketch the C-profile on the top face of the base and extrude upwards
# The web is centered on the base width for this model

# Calculate profile coordinates relative to the center of the base
# We orient the "C" such that the flat face points to +Y (Front)
y_front = wall_thickness / 2.0
y_back_web = -wall_thickness / 2.0
y_back_flange = y_front - flange_depth
x_outer = length / 2.0
x_inner = x_outer - wall_thickness

# Define the points for the C-shape profile (clockwise)
profile_pts = [
    (x_outer, y_front),                 # Front Right
    (x_outer, y_back_flange),           # Back Right Outer
    (x_inner, y_back_flange),           # Back Right Inner
    (x_inner, y_back_web),              # Web Right Inner
    (-x_inner, y_back_web),             # Web Left Inner
    (-x_inner, y_back_flange),          # Back Left Inner
    (-x_outer, y_back_flange),          # Back Left Outer
    (-x_outer, y_front)                 # Front Left
]

# Create the wall geometry
wall = (
    base.faces(">Z").workplane()
    .polyline(profile_pts)
    .close()
    .extrude(wall_height)
)

# 3. Create the holes on the front face
# Calculate hole positions relative to the center of the vertical face
h_x = length / 2.0 - hole_margin_x
h_y = wall_height / 2.0 - hole_margin_z

result = (
    wall.faces(">Y").workplane()
    .pushPoints([
        (h_x, h_y),
        (h_x, -h_y),
        (-h_x, h_y),
        (-h_x, -h_y)
    ])
    .hole(hole_diameter)
)