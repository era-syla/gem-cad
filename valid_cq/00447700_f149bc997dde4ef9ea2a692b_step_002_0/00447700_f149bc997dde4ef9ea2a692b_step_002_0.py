import cadquery as cq

# Parametric dimensions for the model
# Based on the visual approximation of a rectangular component with features
length = 40.0       # Overall length of the base
width = 25.0        # Overall width of the base
thickness = 4.0     # Thickness of the plate
corner_fillet = 2.0 # Radius for corner fillets
hole_diam = 3.0     # Diameter of mounting holes
hole_dist_x = 30.0  # Distance between holes lengthwise
hole_dist_y = 15.0  # Distance between holes widthwise

# Feature dimensions for the raised block (resembling the dark rectangular shape)
block_l = 15.0
block_w = 10.0
block_h = 3.0

# 1. Create the base plate
base = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")
    .fillet(corner_fillet)
)

# 2. Add mounting holes (representing the small specks/details)
# We create a rectangular pattern of points and drill holes
base_with_holes = (
    base.faces(">Z")
    .workplane()
    .rect(hole_dist_x, hole_dist_y, forConstruction=True)
    .vertices()
    .hole(hole_diam)
)

# 3. Add the raised rectangular feature on top (representing the main dark blob)
# Centered on the plate
result = (
    base_with_holes.faces(">Z")
    .workplane()
    .center(0, 0) # Adjust offset if the blob is off-center in interpretation
    .rect(block_l, block_w)
    .extrude(block_h)
)

# Optional: Add a small chamfer to the top block for detail
result = result.edges("|Z").chamfer(0.5)