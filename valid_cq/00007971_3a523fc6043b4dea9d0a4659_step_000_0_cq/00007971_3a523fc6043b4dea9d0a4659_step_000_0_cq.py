import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
length = 150.0
width = 40.0
thickness = 6.0  # Thickness of a single plate
layer_gap = 2.0  # Gap between top and bottom plates (if modeled as an assembly)
total_height = thickness * 2 + layer_gap # Simplified as a solid block with a slot for this exercise

# Slot dimensions
long_slot_length = 80.0
long_slot_width = 4.0
short_slot_length = 30.0
short_slot_width = 4.0
short_slot_offset_y = 10.0 # Offset from center line

# Mounting hole parameters
hole_dia = 2.5
hole_spacing_x_outer = 130.0 # Distance between outer mounting holes
hole_spacing_x_inner = 50.0 # Distance for inner set of holes
hole_spacing_y = 32.0

# Side block (guide/rail) dimensions
side_block_length = 30.0
side_block_width = 8.0
side_block_thickness = 4.0
side_block_pos_x1 = -40.0
side_block_pos_x2 = 40.0

# Pivot tab dimensions
tab_width = 6.0
tab_height = 8.0
tab_thickness = 4.0
tab_hole_dia = 3.0

# --- Modeling ---

# 1. Base Plate (representing the sandwich structure as a main block for simplicity, 
#    but adding details to look like the layered assembly in the image)
main_body = (
    cq.Workplane("XY")
    .box(length, width, total_height)
    .edges("|Z")
    .fillet(2.0) # Rounded corners
)

# 2. Create the distinct separation between top and bottom plates (side groove)
# This mimics the "sandwich" look
groove = (
    cq.Workplane("XY")
    .rect(length + 10, width + 10) # Oversized rect
    .extrude(layer_gap)
    .translate((0, 0, 0)) # Centered vertically
)

# Cut the groove to create top/bottom plate appearance
# Note: box is centered at (0,0,0) so Z goes from -total_height/2 to +total_height/2
# We want the groove in the middle.
main_body = main_body.cut(groove)

# 3. Cut the Long Center Slot
main_body = (
    main_body.faces(">Z")
    .workplane()
    .center(10, 0) # Shift slightly right like in image
    .slot2D(long_slot_length, long_slot_width)
    .cutBlind(-total_height)
)

# 4. Cut the Short Offset Slot (Top Left in image orientation)
main_body = (
    main_body.faces(">Z")
    .workplane()
    .center(-45, short_slot_offset_y) # Approximate position based on image
    .slot2D(short_slot_length, short_slot_width)
    .cutBlind(-thickness) # Only through top plate
)

# 5. Add small mounting holes
# Creating a list of points relative to the top face center
holes = [
    (-length/2 + 5, -width/2 + 5), (-length/2 + 5, width/2 - 5), # Left corners
    (length/2 - 5, -width/2 + 5), (length/2 - 5, width/2 - 5),   # Right corners
    (-15, -10), (-15, 10), # Inner pair 1
    (25, -10), (25, 10),   # Inner pair 2
    (60, 0) # Single hole near right end
]

main_body = (
    main_body.faces(">Z")
    .workplane()
    .pushPoints(holes)
    .hole(hole_dia)
)

# 6. Add Side Guide Blocks (underneath/side)
# Looking at the image, there are blocks sticking out the side/bottom
side_guide_1 = (
    cq.Workplane("XY")
    .box(side_block_length, side_block_width, side_block_thickness)
    .translate((side_block_pos_x1, -width/2 - side_block_width/2, -total_height/2 - side_block_thickness/2))
)

side_guide_2 = (
    cq.Workplane("XY")
    .box(side_block_length, side_block_width, side_block_thickness)
    .translate((side_block_pos_x2, -width/2 - side_block_width/2, -total_height/2 - side_block_thickness/2))
)

# Add chamfers or internal cuts to side guides to match the "U" shape in image
side_guide_cutout = (
    cq.Workplane("XY")
    .box(side_block_length - 4, side_block_width - 2, side_block_thickness + 2)
)

side_guide_1 = side_guide_1.cut(
    side_guide_cutout.translate((side_block_pos_x1, -width/2 - side_block_width/2, -total_height/2 - side_block_thickness/2))
)
side_guide_2 = side_guide_2.cut(
    side_guide_cutout.translate((side_block_pos_x2, -width/2 - side_block_width/2, -total_height/2 - side_block_thickness/2))
)

# 7. Add Vertical Tab (Pivot)
# Located near the left end
tab = (
    cq.Workplane("XZ")
    .center(-length/2 + 15, total_height/2)
    .lineTo(tab_width, 0)
    .lineTo(tab_width, tab_height)
    .threePointArc((tab_width/2, tab_height + tab_width/2), (0, tab_height))
    .close()
    .extrude(tab_thickness)
    .translate((0, tab_thickness/2, 0)) # Center on Y axis
)

# Hole in tab
tab = (
    tab.faces(">Y")
    .workplane()
    .center(0, tab_height) # Move to arc center
    .hole(tab_hole_dia)
)

# Combine everything
result = main_body.union(side_guide_1).union(side_guide_2).union(tab)

# Optional: Add the rectangular cutout on the right end visible in the cross-section
end_cutout = (
    cq.Workplane("YZ")
    .rect(width - 10, total_height - 4)
    .extrude(10)
    .translate((length/2, 0, 0))
)
result = result.cut(end_cutout)