import cadquery as cq

# --- Parametric Dimensions ---
# Base plate dimensions
plate_length = 60.0
plate_width = 30.0
plate_thickness = 5.0
corner_radius = 2.0

# Mounting holes
hole_diameter = 6.0
hole_spacing = 40.0  # Distance between centers

# Hexagonal boss
hex_flat_to_flat = 16.0  # Common size (e.g., for M10 or similar hardware)
hex_height = 15.0        # Height above the plate

# Central bore
bore_diameter = 10.0

# --- Modeling ---

# 1. Create the base plate with rounded corners
# We start with a rectangle, extrude it, and fillet vertical edges
base = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Add the hexagonal boss
# We draw a polygon on the top face of the base
hex_boss = (
    base.faces(">Z")
    .workplane()
    .polygon(nSides=6, diameter=hex_flat_to_flat / 0.866025) # diameter here is usually corner-to-corner. flat_to_flat = diameter * cos(30) -> d = f / cos(30)
    .extrude(hex_height)
)

# 3. Create the mounting holes
# We select the top face (or bottom, doesn't matter for through holes) and cut holes
with_mounting_holes = (
    hex_boss.faces("<Z") # Select bottom face for reference
    .workplane()
    .pushPoints([(-hole_spacing / 2, 0), (hole_spacing / 2, 0)])
    .hole(hole_diameter)
)

# 4. Create the central bore
# This goes through the entire assembly
final_part = (
    with_mounting_holes.faces(">Z") # Select top of the hex boss
    .workplane()
    .hole(bore_diameter)
)

# Assign to result variable
result = final_part