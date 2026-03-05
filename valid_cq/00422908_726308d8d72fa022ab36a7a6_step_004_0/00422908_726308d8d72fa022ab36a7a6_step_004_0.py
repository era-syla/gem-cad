import cadquery as cq

# --- Parameters ---
length = 1000.0      # Total length of the rail
height = 30.0        # Height of the vertical leg (face with holes)
width = 15.0         # Width of the horizontal flange
thickness = 3.0      # Thickness of the material
hole_diameter = 5.0  # Diameter of the mounting holes
num_holes = 20       # Total number of holes
end_padding = 25.0   # Distance from the end of the rail to the first hole center

# --- Geometry Generation ---

# 1. Create the L-profile base
# Drawn on the YZ plane (Side view), extruded along the X axis (Length).
# Origin (0,0,0) is at the bottom-back corner.
# Vertical leg goes up Z, Horizontal leg goes along Y.
rail_profile = (
    cq.Workplane("YZ")
    .lineTo(0, height)              # Up the back face
    .lineTo(thickness, height)      # Top thickness
    .lineTo(thickness, thickness)   # Down to inner corner
    .lineTo(width, thickness)       # Out along the flange
    .lineTo(width, 0)               # Down flange thickness
    .close()                        # Back to origin
)

base_solid = rail_profile.extrude(length)

# 2. Define Hole Locations
# Calculate points along the X-axis centered vertically on the leg (Z-axis).
hole_pitch = (length - 2 * end_padding) / (num_holes - 1)
hole_z_center = height / 2.0

points = []
for i in range(num_holes):
    x_pos = end_padding + i * hole_pitch
    points.append((x_pos, hole_z_center))

# 3. Cut Holes
# Create a tool object on the XZ plane (back face of the rail)
# and extrude cylinders through the vertical leg (in +Y direction).
hole_cutters = (
    cq.Workplane("XZ")
    .pushPoints(points)
    .circle(hole_diameter / 2.0)
    .extrude(thickness * 2)  # Extrude deeper than thickness to ensure clean cut
)

# Apply the cut to the base solid
result = base_solid.cut(hole_cutters)