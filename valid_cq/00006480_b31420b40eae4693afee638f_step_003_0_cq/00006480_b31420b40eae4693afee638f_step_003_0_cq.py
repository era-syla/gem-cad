import cadquery as cq

# --- Parameters ---

# Main Box
box_length = 30.0
box_width = 25.0
box_height = 15.0
wall_thickness = 2.0
bottom_opening_length = 15.0
bottom_opening_width = 10.0

# Side Lug
lug_width = 10.0
lug_depth = 10.0  # Protrusion from the box
lug_height = 10.0
diamond_hole_size = 4.0  # Side of the diamond square

# Lid
lid_thickness = 2.0
lid_corner_radius = 2.0

# Snap Fit / Slot details
snap_width = 6.0
snap_thickness = 1.5
snap_depth = 4.0 # How far down the snap goes
slot_width = snap_width + 0.4
slot_height = 2.0 
slot_z_offset = -3.0 # Distance from top edge

# Ball Joint / Pin Accessory
ball_radius = 6.0
pin_length = 15.0
pin_side = 4.0 # Square cross section

# --- Modeling ---

# 1. The Main Box Case
# Create outer shell
box = (
    cq.Workplane("XY")
    .box(box_length, box_width, box_height)
    # Shell it, leaving the top open
    .faces("+Z")
    .shell(wall_thickness)
)

# Cut the rectangular hole in the bottom
bottom_cutout = (
    cq.Workplane("XY")
    .rect(bottom_opening_length, bottom_opening_width)
    .extrude(wall_thickness * 2) # Make sure it cuts through
    .translate((0, 0, -box_height/2 - wall_thickness))
)
box = box.cut(bottom_cutout)

# Create side slots for the lid snaps
# We need slots on the shorter sides (faces along X axis, normals +/- Y)
slot_cutter = (
    cq.Workplane("XZ")
    .rect(slot_width, slot_height)
    .extrude(box_width + wall_thickness * 2) # Through all
    .translate((0, box_height/2 + slot_z_offset, 0)) # Position relative to top
)
box = box.cut(slot_cutter)


# 2. The Side Lug
# Attached to one of the long sides (face along Y axis, normal +X)
lug = (
    cq.Workplane("YZ")
    .rect(lug_width, lug_height)
    .extrude(lug_depth)
    .translate((box_length/2, 0, -box_height/2 + lug_height/2)) # Align with bottom edge
)

# Diamond hole in the lug
diamond_sketch = (
    cq.Workplane("YZ")
    .rect(diamond_hole_size, diamond_hole_size)
    .rotate((0,0,0), (1,0,0), 45) # Rotate 45 degrees around X (local Z for YZ plane)
)
lug = lug.cut(
    diamond_sketch.extrude(lug_depth + 1)
    .translate((box_length/2 - 0.5, 0, -box_height/2 + lug_height/2))
)

# Combine box and lug
box_assembly = box.union(lug)


# 3. The Lid
lid_base = (
    cq.Workplane("XY")
    .box(box_length, box_width, lid_thickness)
    .edges("|Z")
    .fillet(lid_corner_radius)
)

# Add snaps to the lid
# Snap on -Y side
snap_1 = (
    cq.Workplane("XZ")
    .rect(snap_width, snap_thickness)
    .extrude(-snap_depth) # Extrude downwards
    .translate((0, box_height/2, -box_width/2 + wall_thickness/2)) # Position roughly
    # Refine position: centered on side wall
    .translate((0, 0, 0)) 
)

# Create a simple hook profile for the snap
def create_snap_hook(loc_y_offset):
    hook_prof = (
        cq.Workplane("YZ")
        .moveTo(0, 0)
        .lineTo(0, -snap_depth)
        .lineTo(wall_thickness/2, -snap_depth) # The hook part
        .lineTo(wall_thickness/2, -snap_depth + 1.0)
        .lineTo(snap_thickness, -snap_depth + 1.5) # Taper back
        .lineTo(snap_thickness, 0)
        .close()
    )
    return hook_prof.extrude(snap_width/2, both=True).translate((0, loc_y_offset, -lid_thickness/2))

# Since the image shows simple rectangular tabs with holes in the box, 
# let's model the snaps as simple downward protrusions that would flex into the slots.
# Actually, looking closer at the image, the lid has rectangular cutouts, 
# and the *box* has the tabs? Or the lid has tabs that go into the slots.
# Let's assume the lid has tabs that go *down* into the box slots.

snap_tab_shape = (
    cq.Workplane("XY")
    .rect(snap_width, snap_thickness)
    .extrude(- (abs(slot_z_offset) + slot_height))
    .translate((0, -box_width/2 + wall_thickness/2, -lid_thickness/2))
)
# Create the little bump on the tab that locks into the slot
snap_bump = (
    cq.Workplane("XZ")
    .moveTo(-snap_width/2, 0)
    .lineTo(snap_width/2, 0)
    .lineTo(0, slot_height/2)
    .close()
    .extrude(1.0) # Depth of the bump
    .rotate((1,0,0), (0,0,0), -90)
    .translate((0, -box_width/2 + wall_thickness, -lid_thickness/2 + slot_z_offset - slot_height/2))
)

# Mirror for the other side
snap_assembly = snap_tab_shape # .union(snap_bump) # Simplified for visual match to image (bump is internal usually)
snap_assembly_mirrored = snap_assembly.mirror("XZ")

lid_assembly = lid_base.union(snap_assembly).union(snap_assembly_mirrored)

# Position Lid above box
lid_assembly = lid_assembly.translate((0, 0, box_height/2 + lid_thickness/2 + 10))


# 4. Ball Joint Accessory
# Square shaft
shaft = (
    cq.Workplane("XY")
    .rect(pin_side, pin_side)
    .extrude(pin_length)
    .rotate((0,1,0), (0,0,0), 90) # Orient along X
)

# Ball
sphere = (
    cq.Workplane("XY")
    .sphere(ball_radius)
    .translate((pin_length, 0, 0)) # Move to end of shaft
    # Flatten the end of the sphere slightly as seen in image
    .cut(
        cq.Workplane("YZ")
        .rect(ball_radius*2, ball_radius*2)
        .extrude(ball_radius)
        .translate((pin_length + ball_radius - 1.0, 0, 0))
    )
)

accessory = shaft.union(sphere).translate((box_length/2 + 10, 0, box_height + 15))


# --- Final Assembly ---
result = box_assembly.union(lid_assembly).union(accessory)