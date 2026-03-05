import cadquery as cq

# Define parametric dimensions based on the visual proportions
height = 80.0
width = 50.0
thickness = 10.0
notch_height = 20.0
notch_depth = 8.0

# Create the base rectangular block
# We orient the block standing up (Z-axis is height)
# width along X, thickness along Y, height along Z
result = cq.Workplane("XY").box(width, thickness, height)

# Create the notch on the side edge
# 1. Select the face on the positive X direction (the right edge)
# 2. Create a new workplane on this face
# 3. Draw a rectangle representing the material to be removed.
#    We make the rectangle wider than the thickness to ensure a clean cut through the Y-axis.
# 4. Cut blindly into the block (negative direction relative to the face normal)
result = (
    result.faces(">X")
    .workplane()
    .rect(thickness * 2, notch_height)
    .cutBlind(-notch_depth)
)