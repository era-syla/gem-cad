import cadquery as cq

# -- Parameters --
# Plate dimensions
plate_width = 80.0
plate_length = 130.0
plate_thickness = 5.0
corner_radius = 5.0

# Hole definitions (positions and diameters)
# The coordinate system is assumed to be centered on the plate's top face for easier hole placement.
# Coordinates are (x, y).

# Main mounting holes (likely V-slot gantry plate style)
# Four holes forming a rough rectangle, but not perfectly symmetric in the image
hole_positions_1 = [
    (-20, -40),  # Bottom Left
    (20, -40),   # Bottom Right
    (-20, 40),   # Top Left
    (20, 40)     # Top Right
]
hole_diameter_1 = 5.0 # M5 clearance

# Additional mounting holes (offset closer to center)
hole_positions_2 = [
    (-20, 0),    # Left Middle
    (20, 20),    # Right Top Offset
    (20, -20)    # Right Bottom Offset
]
hole_diameter_2 = 5.0 # M5 clearance

# Larger central-ish hole
center_hole_pos = (20, 0)
center_hole_dia = 7.1 # Typically an eccentric spacer hole (often around 7mm or 7.1mm)

# Small corner/edge holes
corner_hole_positions = [
    (30, 55),    # Top Right Corner
    (30, -55)    # Bottom Right Corner
]
corner_hole_dia = 5.0

# -- Modeling --

# 1. Create the base plate with rounded corners
plate = (
    cq.Workplane("XY")
    .box(plate_width, plate_length, plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Add the first set of holes
result = (
    plate
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions_1)
    .hole(hole_diameter_1)
)

# 3. Add the second set of holes
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions_2)
    .hole(hole_diameter_2)
)

# 4. Add the larger eccentric spacer hole
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([center_hole_pos])
    .hole(center_hole_dia)
)

# 5. Add the outer edge holes
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(corner_hole_positions)
    .hole(corner_hole_dia)
)

# Export is not requested, but 'result' variable is required.