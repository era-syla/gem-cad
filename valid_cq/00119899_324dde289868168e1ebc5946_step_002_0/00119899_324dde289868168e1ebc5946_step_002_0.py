import cadquery as cq

# --- Parameters ---
# Dimensions estimated from the image
total_length = 80.0
outer_diameter = 8.0
radius = outer_diameter / 2.0

# Top detail dimensions
chamfer_size = 0.4
bore_diameter = 3.0
bore_depth = 6.0
notch_width = 1.5
notch_depth = 2.5

# --- Modeling Process ---

# 1. Create the base cylinder
# We start by drawing a circle on the XY plane and extruding it to the total length.
result = cq.Workplane("XY").circle(radius).extrude(total_length)

# 2. Add the chamfer to the top edge
# We select the top face (Max Z) and then its edges. 
# At this stage, the top face only has the outer circular edge.
result = result.faces(">Z").edges().chamfer(chamfer_size)

# 3. Cut the central blind hole
# We select the top face again to establish a workplane, draw the bore circle, and cut down.
result = result.faces(">Z").workplane().circle(bore_diameter / 2.0).cutBlind(-bore_depth)

# 4. Cut the cross-shaped notches
# We select the top face again.
# We draw two overlapping rectangles centered at the origin to form a cross.
# The length of the rectangles is set larger than the diameter to ensure they cut through the outer edge completely.
result = (
    result.faces(">Z")
    .workplane()
    .rect(notch_width, outer_diameter * 2.0)  # Vertical slot
    .rect(outer_diameter * 2.0, notch_width)  # Horizontal slot
    .cutBlind(-notch_depth)
)