import cadquery as cq
import math

# Parametric dimensions
edge_length = 20.0  # Length of each side of the hexagonal basis
thickness = 10.0    # Extrusion height

# Calculate geometric offsets based on 60-degree equilateral geometry
# This shape is geometrically equivalent to a hexagon with one triangular sector removed (or moved to center)
h = edge_length * math.sin(math.radians(60))
dx = edge_length * math.cos(math.radians(60))

# Define vertices for the chevron/arrow shape
# Points are defined counter-clockwise starting from the right-most tip
points = [
    (edge_length, 0.0),      # Right Tip
    (dx, h),                 # Top Right Corner
    (-dx, h),                # Top Left Corner
    (0.0, 0.0),              # Center Notch (Re-entrant corner)
    (-dx, -h),               # Bottom Left Corner
    (dx, -h)                 # Bottom Right Corner
]

# Generate the 3D solid
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)