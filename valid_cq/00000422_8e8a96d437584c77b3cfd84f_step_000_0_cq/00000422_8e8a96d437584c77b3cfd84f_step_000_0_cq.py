import cadquery as cq

# Parametric dimensions
plate_thickness = 5.0

# Dimensions for the "T" shape
# Main body (the crossbar of the T)
main_width = 60.0   # Width of the wider part
main_length = 40.0  # Length (depth) of the wider part

# Stem (the vertical part of the T)
stem_width = 30.0   # Width of the narrower part
stem_length = 30.0  # Length (depth) of the extension

# Hole details
hole_diameter = 6.0
hex_hole_width = 12.0  # Distance across flats for the hex recess
hex_depth = 3.0       # Depth of the hex recess

# Create the T-shape base
# We'll construct this by unioning two rectangles or cutting a larger one.
# Method: Union two rectangles centered appropriately.

# 1. The wider rectangle (bottom part of the T in typical view, top part in this specific orientation)
# Let's align the center of the main body to origin for now to make hole placement easier.
base = cq.Workplane("XY").box(main_width, main_length, plate_thickness)

# 2. The stem rectangle
# We need to position this relative to the main body.
# If the main body is centered at (0,0), its Y extends from -20 to +20.
# We want to add the stem to one side. Let's add it to the -Y direction.
stem = (
    cq.Workplane("XY")
    .center(0, -main_length/2 - stem_length/2)
    .box(stem_width, stem_length, plate_thickness)
)

# Combine them
part = base.union(stem)

# Locate the hole
# The hole appears to be centered on the main wide part of the plate.
# Since we centered the main_width/main_length box at (0,0), the hole should be at (0,0).

# Create the counterbored hex hole
# First, the through hole
part = part.faces(">Z").workplane().hole(hole_diameter)

# Next, the hexagonal recess
# We need a hexagonal polygon sketch extruded down (cut)
part = (
    part.faces(">Z")
    .workplane()
    .polygon(nSides=6, diameter=hex_hole_width / 0.866025) # Convert flats to corners (approx 2/sqrt(3))
    .cutBlind(-hex_depth)
)

# Assign to result
result = part