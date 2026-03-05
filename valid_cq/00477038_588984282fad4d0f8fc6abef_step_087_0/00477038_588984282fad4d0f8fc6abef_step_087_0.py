import cadquery as cq

# Parameters for the mounting plate
length = 200.0
width = 140.0
thickness = 4.0
fillet_radius = 5.0
notch_radius = 15.0
notch_offset_x = -30.0  # Position of the side notches relative to center X
hole_diameter = 4.0

# List of (x, y) coordinates for the mounting holes
# Coordinates estimated based on the visual pattern in the image
hole_positions = [
    # Corner holes
    (-length/2 + 10, width/2 - 10),    # Top-Left
    (length/2 - 10, width/2 - 10),     # Top-Right
    (-length/2 + 10, -width/2 + 10),   # Bottom-Left
    (length/2 - 10, -width/2 + 10),    # Bottom-Right (Corner)
    
    # Extra hole near Bottom-Right corner (as seen in image)
    (length/2 - 10, -width/2 + 25),
    
    # Holes near the notches
    (notch_offset_x - 25, width/2 - 12),
    (notch_offset_x - 25, -width/2 + 12),
    
    # Central / Internal mounting holes pattern
    (0, 20),
    (0, -20),
    (40, 0),
    (-10, 0),
    (50, 30),
    (50, -30)
]

# 1. Create the base rectangular plate with filleted corners
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)

# 2. Create the U-shaped notches on the long sides
# We position circles on the edges of the plate and cut through
result = (
    result.faces(">Z")
    .workplane()
    .moveTo(notch_offset_x, width/2)
    .circle(notch_radius)
    .moveTo(notch_offset_x, -width/2)
    .circle(notch_radius)
    .cutThruAll()
)

# 3. Drill the mounting holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .circle(hole_diameter / 2)
    .cutThruAll()
)