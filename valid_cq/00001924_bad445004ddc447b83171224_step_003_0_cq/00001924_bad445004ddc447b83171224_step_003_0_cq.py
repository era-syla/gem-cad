import cadquery as cq

# --- Parameters ---
plate_width = 100.0
plate_depth = 100.0
plate_thickness = 5.0
corner_radius = 5.0

# Strap slot parameters
slot_length = 20.0
slot_width = 4.0
slot_inset_x = 10.0 # From the side edge
slot_inset_y = 10.0 # From the back edge

# Front ridge/bumper parameters
bumper_width = 15.0 # Width of the raised front section
bumper_height = 2.0 # Extra height above plate
bumper_gap_width = 1.0 # The gap between main plate and bumper

# Center clip/latch mechanism parameters
latch_width = 12.0
latch_depth = 12.0
latch_height = 4.0 # Height above plate
latch_chamfer = 2.0
latch_center_gap = 1.0

# Bottom feet parameters
foot_size = 6.0
foot_height = 4.0
foot_inset = 4.0

# Small holes on bumper
hole_diameter = 2.0
hole_offset_x = 10.0 # From side edge

# --- Construction ---

# 1. Main Base Plate
# Create the base rectangle
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_depth)
    .extrude(plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Add Front Bumper Section
# It looks like a separate strip at the front, or part of the same mold separated by a groove.
# Let's model it as an addition on top for the extra height.

bumper_y_pos = -plate_depth/2 + bumper_width/2

bumper = (
    cq.Workplane("XY")
    .center(0, bumper_y_pos)
    .rect(plate_width, bumper_width)
    .extrude(plate_thickness + bumper_height)
    .edges("|Z")
    .fillet(corner_radius)
)

# Combine base and bumper basics (though usually they are one piece)
# In this specific design, there's a distinct groove separating the main plate area from the front bumper area.
# So let's cut the groove.

groove_y_pos = -plate_depth/2 + bumper_width
result = base.union(bumper)

# Cut the groove separating the main plate from the front bumper
# The groove runs across X
groove_cutter = (
    cq.Workplane("XY")
    .center(0, -plate_depth/2 + bumper_width)
    .rect(plate_width + 10, bumper_gap_width) # Make it wider than plate to cut through
    .extrude(plate_thickness) # Cut deep enough
)

# We actually want the groove to go down a bit but maybe not all the way through?
# Looking closely, it looks like a deep relief cut or a through cut with connecting ribs. 
# Let's assume a deep relief cut from the top.
groove_depth = 2.0
groove_cutter = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness + bumper_height)
    .center(0, -plate_depth/2 + bumper_width)
    .rect(plate_width + 10, bumper_gap_width)
    .extrude(-groove_depth * 2) # Cut downwards
)

# However, the image shows the bumper is flush on the bottom but raised on top.
# Let's redefine the strategy:
# Start with the main shape, then cut slots and add features.

# Re-strategy:
# 1. Main body block
main_body = (
    cq.Workplane("XY")
    .rect(plate_width, plate_depth)
    .extrude(plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Add the raised bumper strip
bumper_addition = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness)
    .center(0, -plate_depth/2 + bumper_width/2)
    .rect(plate_width, bumper_width)
    .extrude(bumper_height)
    .edges("|Z").fillet(corner_radius) # Match corner radius
)

result = main_body.union(bumper_addition)

# 3. Cut the transverse groove
groove = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness + bumper_height)
    .center(0, -plate_depth/2 + bumper_width)
    .rect(plate_width * 1.2, bumper_gap_width)
    .extrude(-3.0) # Cut down into the material
)
result = result.cut(groove)

# 4. Create Strap Slots (Rear corners)
slot_x_center = plate_width/2 - slot_inset_x - slot_length/2
slot_y_center = plate_depth/2 - slot_inset_y

# Create a single slot cutter
slot_cutter = (
    cq.Workplane("XY")
    .rect(slot_length, slot_width)
    .extrude(plate_thickness * 3)
)

# Cut left slot
result = result.cut(
    slot_cutter.translate((-slot_x_center, slot_y_center, -plate_thickness))
)

# Cut right slot
result = result.cut(
    slot_cutter.translate((slot_x_center, slot_y_center, -plate_thickness))
)

# 5. Center Latch Mechanism
# This sits on the groove line. It's a raised block with a split.
latch_y_pos = -plate_depth/2 + bumper_width 

latch_block = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness) # Start on top of base plate
    .center(0, latch_y_pos)
    .rect(latch_width, latch_depth)
    .extrude(latch_height)
)

# Add chamfers to the latch block sides (sloped appearance)
# We select edges parallel to Y on the top face
latch_block = (
    latch_block.faces(">Z")
    .edges("|Y")
    .chamfer(latch_chamfer)
)

# Cut the split in the middle of the latch (continuation of the groove)
latch_split = (
    cq.Workplane("XY")
    .center(0, latch_y_pos)
    .rect(latch_center_gap, latch_depth * 1.5)
    .extrude(plate_thickness + latch_height + 5)
)

latch_final = latch_block.cut(latch_split)
result = result.union(latch_final)

# 6. Small alignment holes on the bumper
hole_x_pos = plate_width/2 - hole_offset_x
hole_y_pos = -plate_depth/2 + bumper_width/2

result = (
    result.faces(">Z").workplane()
    .pushPoints([(-hole_x_pos, hole_y_pos), (hole_x_pos, hole_y_pos)])
    .hole(hole_diameter, depth=5.0)
)

# 7. Bottom Feet
# Four feet at the corners
foot_x = plate_width/2 - foot_inset - foot_size/2
foot_y_front = -plate_depth/2 + foot_inset + foot_size/2
foot_y_back = plate_depth/2 - foot_inset - foot_size/2 # Although image only clearly shows front feet

# Let's create a generic foot shape (tapered square)
def create_foot(x, y):
    return (
        cq.Workplane("XY")
        .center(x, y)
        .rect(foot_size, foot_size)
        .extrude(-foot_height)
        .faces("<Z").edges().fillet(1.0) # Soften bottom edges
    )

# The image shows feet primarily under the front corners clearly. Assuming 4 feet for stability.
# Front Left
result = result.union(create_foot(-foot_x, foot_y_front))
# Front Right
result = result.union(create_foot(foot_x, foot_y_front))
# Back Left (Assuming symmetry)
# result = result.union(create_foot(-foot_x, foot_y_back))
# Back Right (Assuming symmetry)
# result = result.union(create_foot(foot_x, foot_y_back))

# Looking at the image again, the feet seem to be specifically under the bumper section.
# Let's stick to the visible front feet.

# Final cleanup
# Ensure the cut groove goes through the latch area correctly?
# The boolean cut previously might have been filled by the union of the latch.
# Let's re-cut the groove specifically through the latch area if needed, 
# but the latch_split handles the center. The transverse groove is interrupted by the latch base.
# The code sequence handles this correctly (union latch, then split latch).

# Export result
if 'show_object' in locals():
    show_object(result)