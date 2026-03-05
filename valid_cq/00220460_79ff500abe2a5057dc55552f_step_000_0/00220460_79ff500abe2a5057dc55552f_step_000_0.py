import cadquery as cq

# Parametric dimensions for the structural C-channel/strut profile
length = 800.0      # Total length of the extrusion
width = 41.0        # Outer width of the profile
height = 41.0       # Outer height of the profile
thickness = 2.5     # Wall thickness
lip_width = 8.0     # Width of the inward-facing lips

# Calculate half-width for symmetry
w_half = width / 2.0

# Define points for the cross-section starting from bottom-left corner
# The profile is a C-shape with lips at the top
points = [
    (-w_half, 0),                                    # Bottom-left outer
    (w_half, 0),                                     # Bottom-right outer
    (w_half, height),                                # Top-right outer
    (w_half - lip_width, height),                    # Right lip end (top)
    (w_half - lip_width, height - thickness),        # Right lip end (bottom)
    (w_half - thickness, height - thickness),        # Right inner wall (top)
    (w_half - thickness, thickness),                 # Right inner wall (bottom)
    (-w_half + thickness, thickness),                # Left inner wall (bottom)
    (-w_half + thickness, height - thickness),       # Left inner wall (top)
    (-w_half + lip_width, height - thickness),       # Left lip end (bottom)
    (-w_half + lip_width, height),                   # Left lip end (top)
    (-w_half, height)                                # Top-left outer
]

# Generate the 3D model
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(length)
)