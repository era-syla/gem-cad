import cadquery as cq

# Parametric dimensions
height = 120.0          # Height of the vertical curved wall
outer_radius = 60.0     # Outer radius of the curve
thickness = 5.0         # Thickness of the material (wall and base)
base_flange_width = 40.0 # Width of the horizontal base leg

# derived parameters for the sketch coordinates
r_outer = outer_radius
r_inner_wall = outer_radius - thickness
r_inner_base = outer_radius - base_flange_width

# Ensure inner radius is non-negative
if r_inner_base < 0:
    r_inner_base = 0

# Define the points of the L-profile cross-section
# The sketch is drawn on the XZ plane.
# Local X corresponds to radial distance from the Z-axis.
# Local Y corresponds to height (Z).
points = [
    (r_inner_base, 0),              # Bottom inner point of the base
    (r_outer, 0),                   # Bottom outer corner
    (r_outer, height),              # Top outer corner
    (r_inner_wall, height),         # Top inner point of the wall
    (r_inner_wall, thickness),      # Inner corner junction
    (r_inner_base, thickness)       # Top inner point of the base
]

# Generate the model
# 1. Create a workplane on XZ
# 2. Draw the L-shaped profile
# 3. Revolve 90 degrees around the Z-axis (Local Y of the XZ plane)
result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .revolve(90, (0, 0, 0), (0, 1, 0))
)