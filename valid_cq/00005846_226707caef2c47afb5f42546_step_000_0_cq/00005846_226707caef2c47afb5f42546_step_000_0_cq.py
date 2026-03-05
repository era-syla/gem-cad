import cadquery as cq

# --- Parameter Definitions ---

# 1. Main Block Parameters
block_length = 80.0
block_width = 50.0
block_height = 25.0
block_fillet_radius = 5.0

# 2. Square Plate Parameters
plate_side = 30.0
plate_thickness = 2.0
plate_center_hole_dia = 15.0
plate_corner_hole_dia = 3.0
# Calculate spacing for corner holes (centered relative to corners)
plate_hole_margin = 4.0
plate_hole_offset = plate_side/2 - plate_hole_margin

# 3. Clip Parameters
clip_outer_dia = 10.0
clip_inner_dia = 7.0
clip_height = 5.0
clip_opening_width = 5.0

# --- Geometry Construction ---

# 1. Create the Main Block
# A simple box with fillets on the vertical edges
block = (
    cq.Workplane("XY")
    .box(block_length, block_width, block_height)
    .edges("|Z")
    .fillet(block_fillet_radius)
)

# 2. Create the Square Plate
# A square extrusion with a large center hole and 4 corner holes
plate = (
    cq.Workplane("XY")
    .rect(plate_side, plate_side)
    .extrude(plate_thickness)
    .faces(">Z")
    .workplane()
    # Center hole
    .circle(plate_center_hole_dia / 2)
    .cutThruAll()
    # Corner holes
    .faces(">Z")
    .workplane()
    .rect(plate_hole_offset * 2, plate_hole_offset * 2, forConstruction=True)
    .vertices()
    .circle(plate_corner_hole_dia / 2)
    .cutThruAll()
)

# 3. Create the Clip
# Two concentric circles to form a ring, then cut a slot
clip = (
    cq.Workplane("XY")
    .circle(clip_outer_dia / 2)
    .circle(clip_inner_dia / 2)
    .extrude(clip_height)
    # Cut the opening slot
    .faces(">Z")
    .workplane()
    .rect(clip_outer_dia + 2, clip_opening_width) # Make the cutter long enough to pass through
    .cutThruAll()
)

# --- Assembly / Positioning ---

# Move the parts to resemble the layout in the image
# The block stays at the origin.
# The clip is moved to the right of the block.
# The plate is moved further to the right.

spacing = 20.0 # Spacing between components

# Position the clip
clip_positioned = clip.translate((block_length/2 + spacing + clip_outer_dia/2, 0, -block_height/2 + clip_height/2))

# Position the plate
plate_positioned = plate.translate((block_length/2 + spacing + clip_outer_dia + spacing + plate_side/2, 0, -block_height/2 + plate_thickness/2))

# Combine all into one result object for visualization
result = block.union(clip_positioned).union(plate_positioned)

# If running in an environment that supports show_object (like CQ-Editor), this line is useful:
# show_object(result)