import cadquery as cq

# --- Parametric Dimensions ---
width = 150.0          # Width of the panel
height = 200.0         # Height of the panel
thickness = 5.0        # Thickness of the panel
hole_diameter = 8.0    # Diameter of the mounting holes
margin_top = 15.0      # Distance from the top edge to hole center
margin_side = 15.0     # Distance from the side edge to hole center

# --- Geometry Generation ---

# 1. Create the base rectangular plate centered at the origin
# The box method creates a prism centered at (0,0,0)
result = cq.Workplane("XY").box(width, height, thickness)

# 2. Calculate hole positions
# Since the box is centered, the top edge is at y = height/2
# and the right edge is at x = width/2
y_pos = (height / 2.0) - margin_top
x_pos = (width / 2.0) - margin_side

# Define the points for the two holes (Top-Left and Top-Right)
hole_locations = [
    (-x_pos, y_pos),
    (x_pos, y_pos)
]

# 3. Create the holes
# Select the top face (>Z), create a workplane on it, push points, and cut holes
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .hole(hole_diameter)
)

# The variable 'result' now contains the final CAD model