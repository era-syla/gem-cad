import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions
total_length = 150.0  # Estimated total length
main_width = 15.0     # Width of the main long bar
total_height = 25.0   # Height of the vertical section

# L-bracket section dimensions
base_thickness = 8.0  # Thickness of the bottom horizontal plate
wall_thickness = 8.0  # Thickness of the vertical wall

# Rounded end details
radius_end = 25.0     # Radius of the larger rounded end

# Cutout details
large_u_cutout_radius = 12.0 # Radius of the U-shaped cutouts
large_u_center_y_offset = 12.0 # Offset from the back wall for U-cutouts

# Hole details
small_hole_dia = 5.0  # Diameter of small mounting holes
large_hole_dia = 8.0  # Diameter of larger side holes

# --- Geometry Construction ---

# 1. Start with the main L-profile base shape
# We'll build this by drawing the profile on the YZ plane and extruding along X
# Or simpler: build two blocks and union them.

# Let's start with the base plate (horizontal part)
# Origin is at the bottom-left-rear corner.
base_plate = cq.Workplane("XY").box(total_length, total_height + 10, base_thickness, centered=False)

# Create the vertical wall
vertical_wall = cq.Workplane("XY").workplane(offset=0).box(total_length, wall_thickness, total_height, centered=False)

# Combine them
main_body = base_plate.union(vertical_wall)

# Refine the shape: The "base plate" isn't a simple rectangle. 
# It has a rounded end and cutouts. Let's redraw the base profile more accurately.

# Strategy 2: Sketch the top-down profile (XY plane) and extrude up, then add the vertical wall features.

# --- Revised Strategy ---

# Step 1: Create the main flat base shape
# The shape is roughly a long rectangle with a rounded head.
# Let's define the profile.

sketch_length = total_length
sketch_width = 30.0 # Width of the wide part at the rounded end

# Create the main block
# Aligned so the back face is at Y=0
base = (
    cq.Workplane("XY")
    .rect(total_length, main_width, centered=False) # Long narrow part
    .extrude(total_height) # This forms the tall back wall
)

# Now add the "shelf" or horizontal extensions
# Front extension 1 (The rounded head)
head_radius = 25.0
head_length = 50.0
head_thickness = 8.0

head = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(head_length, 0)
    .lineTo(head_length, head_radius)
    .lineTo(head_radius, head_radius)
    .radiusArc((0, 0), -head_radius) # Create the rounded corner
    .close()
    .extrude(head_thickness)
)

# Move the head to align correctly (centered circle at origin roughly)
# Adjusting coordinates to match the image relative to the long bar
# Let's shift the head so its curve aligns with the end of the bar.
head = head.translate((0, 0, 0))

# Front extension 2 (The U-shape block in the middle)
mid_block_start = 80.0
mid_block_width = 30.0
mid_block_depth = 20.0
mid_block = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .moveTo(mid_block_start, 0)
    .rect(mid_block_width, mid_block_depth, centered=False)
    .extrude(head_thickness) # Same height as the head shelf
)

# Front extension 3 (The U-shape block at the far end)
end_block_start = 125.0
end_block_width = 25.0
end_block_depth = 15.0 
end_block = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .moveTo(total_length - end_block_width, 0)
    .rect(end_block_width, end_block_depth, centered=False)
    .extrude(head_thickness)
)

# Combine all positive geometry
part = base.union(head).union(mid_block)
# We need to clean up the union to ensure the back wall is consistent
# The 'head' creates a wide area, the 'base' creates the tall narrow wall.

# Let's subtract the excess material from the tall wall to make it L-shaped everywhere
# Actually, it's easier to just union the specific shapes.

# Re-doing the construction for cleanliness:
# 1. The tall back wall (the spine)
spine_thickness = 8.0
spine = cq.Workplane("XY").box(total_length, spine_thickness, total_height, centered=False)

# 2. The flat horizontal shelf features
# Feature A: The rounded head
feat_a = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(50, 0)
    .lineTo(50, 30)
    .lineTo(25, 30)
    .radiusArc((0, 5), -25) # Large radius
    .lineTo(0,0)
    .close()
    .extrude(base_thickness)
)

# Feature B: The middle block with U-cutout
feat_b = (
    cq.Workplane("XY")
    .rect(35, 25, centered=False)
    .extrude(base_thickness)
    .translate((75, 0, 0))
)

# Feature C: The end block
feat_c = (
    cq.Workplane("XY")
    .rect(25, 20, centered=False)
    .extrude(base_thickness)
    .translate((125, 0, 0))
)

# Union the shelf parts
shelves = feat_a.union(feat_b).union(feat_c)

# Union the spine and shelves
result = spine.union(shelves)

# --- Machining Operations (Cuts) ---

# 1. The U-shaped cutout in the middle block (Feat B)
u_cutout_radius = 10.0
u_cutout_center = (75 + 35/2, 25) # Centered on the block, starting from edge
result = result.cut(
    cq.Workplane("XY")
    .workplane(offset=-1) # Start slightly below
    .moveTo(u_cutout_center[0], 35) # Start outside
    .lineTo(u_cutout_center[0] - u_cutout_radius, 35)
    .lineTo(u_cutout_center[0] - u_cutout_radius, 15)
    .radiusArc((u_cutout_center[0] + u_cutout_radius, 15), u_cutout_radius)
    .lineTo(u_cutout_center[0] + u_cutout_radius, 35)
    .close()
    .extrude(base_thickness + 2)
)

# 2. The U-shaped cutout in the head (Feat A) - similar logic
head_u_radius = 12.0
result = result.cut(
    cq.Workplane("XY")
    .workplane(offset=-1)
    .moveTo(50 - 15, 35) 
    .lineTo(50 - 15 - head_u_radius, 35)
    .lineTo(50 - 15 - head_u_radius, 15)
    .radiusArc((50 - 15 + head_u_radius, 15), head_u_radius)
    .lineTo(50 - 15 + head_u_radius, 35)
    .close()
    .extrude(base_thickness + 2)
)

# 3. Holes in the rounded head (Feat A)
# Arc of small holes
result = (
    result.faces("<Z").workplane()
    .pushPoints([(10, 10), (10, 22), (22, 26), (36, 26), (38, 10)])
    .hole(small_hole_dia)
)

# 4. Side holes in the spine/blocks
# Middle block side hole
result = (
    result.faces(">X").workplane(centerOption="CenterOfBoundBox")
    .transformed(offset=(0, -total_height/2 + base_thickness/2, 0)) # Move to shelf level
    .pushPoints([(-10, 0)]) # Relative to end of part
    .hole(large_hole_dia, depth=20)
)

# The middle block actually has a hole going through the side face (X-direction)
# Let's place it manually relative to global coords for precision
result = result.cut(
    cq.Workplane("YZ")
    .workplane(offset=75) # Start of middle block
    .moveTo(15, base_thickness/2)
    .circle(small_hole_dia/2)
    .extrude(35) # Cut through the block width
)
# And the other side of the U-cutout
result = result.cut(
    cq.Workplane("YZ")
    .workplane(offset=75+35) # End of middle block
    .moveTo(15, base_thickness/2)
    .circle(small_hole_dia/2)
    .extrude(-10) # Cut backwards
)

# 5. Hole at the far end block (Feat C) - Through hole Z axis
result = (
    result.faces("<Z").workplane()
    .moveTo(125 + 12.5, 10)
    .hole(large_hole_dia)
)

# 6. Hole on the vertical spine face (Y-direction) at the far end
result = (
    result.faces(">Y").workplane()
    .moveTo(-15, -total_height/2) # approximate location
    .hole(large_hole_dia)
)

# 7. Apply fillets to the back corners of the cutouts
# Selecting vertical edges inside the U-cuts is tricky without tags.
# We will fillet the main outer vertical edge of the spine-shelf junction if needed,
# but the image shows sharp internal corners mostly, except the main radius.

# Clean up intersection of the first U-cut (on the head) which looks distinct in image
# Re-adjusting the head shape cutout to match image better (it cuts into the shelf deep)

# Final check of orientation
# Rotate to match image view (roughly isometric)
# No rotation needed for the model definition, only for viewing.