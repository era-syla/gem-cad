import cadquery as cq

# -- Parametric Dimensions --
plate_length = 140.0       # Total length (X-axis)
plate_width = 90.0         # Total width (Y-axis)
plate_thickness = 4.0      # Thickness (Z-axis)
fillet_radius = 6.0        # Corner radius
hole_diameter = 5.0        # Diameter of the through holes

# Hole Layout Parameters
# Distance from the edge to the center of the corner holes
margin_x = 12.0
margin_y = 12.0

# Calculate hole coordinates relative to center (0,0)
dx = (plate_length / 2) - margin_x
dy = (plate_width / 2) - margin_y

# Define the list of hole centers: 4 corners + 1 center
hole_locations = [
    (-dx, dy),   # Top-Left
    (dx, dy),    # Top-Right
    (0, 0),      # Center
    (-dx, -dy),  # Bottom-Left
    (dx, -dy)    # Bottom-Right
]

# -- Geometry Generation --

# 1. Create the base rectangular plate centered on XY plane
base = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Fillet the four vertical corners
base = base.edges("|Z").fillet(fillet_radius)

# 3. Create the holes
# Select the top face, create a workplane, push the points, and cut through
result = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .hole(hole_diameter)
)