import cadquery as cq

# --- Parameters ---
shaft_diam = 20.0
shaft_length = 80.0

head_width = 30.0   # Width of the blocky part
head_depth = 35.0   # Depth before the curve
head_height = 30.0  # Height of the blocky part
head_arch_radius = 40.0 # Radius for the curved face

boss_diam = 15.0
boss_length = 15.0

# Back mount features (the complex looking part on the back)
mount_width = 20.0
mount_thickness = 5.0
mount_height = head_height * 0.8
rail_groove_depth = 2.0
rail_groove_width = 3.0

# --- Construction ---

# 1. Main Shaft
shaft = cq.Workplane("XY").circle(shaft_diam / 2).extrude(shaft_length)

# 2. The Head Block
# We'll create the head on top of the shaft.
# The head seems to be centered on the shaft in X, but offset in Y.
head_base_plane = shaft.faces(">Z").workplane()

# Let's define the profile of the head. It looks roughly rectangular with a curved front.
# We'll sketch on the YZ plane (side view) to get the curve profile right, then extrude.
# Or simpler: Make a box, then cut the curve, or extrude a specific profile.

# Method: Create a box centered on X, aligned with shaft top.
head_block = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length)
    .box(head_width, head_depth, head_height, centered=(True, False, False))
)
# Move the box so it sits correctly relative to the shaft
# The shaft is centered at (0,0). Let's shift the box in Y so the shaft enters the back/bottom.
head_block = head_block.translate((0, -head_depth/2, 0))

# 3. Create the Curved Front Face
# We will cut the front face with a large cylinder or fillet, but an intersection or loft might be better.
# Looking closely, the front face is convex. It looks like an intersection with a cylinder 
# oriented along the X-axis (or similar).
# Let's try adding a cylinder on the front face to act as the curved surface, or just filleting.
# Actually, it looks like the main body *is* a loft or a specific extrusion.
# Let's refine: It's a box, but the front face (positive Y) is rounded.
# Let's just make a cylinder intersecting a box.

# Alternative Head Construction:
# A box for the back part.
# A cylinder oriented X-axis for the front part? No, the curve is vertical.
# It looks like the top face is curved. Wait, looking at the shadow, the top is flat.
# The face facing the viewer (with the boss) is curved.
# Let's create a block, and then filet the top front edge heavily? No.

# Let's Model the Head as a sketch extruded upwards.
# The profile on the XY plane (looking down) is rectangular.
# The profile from the side (YZ plane) shows the shape best.
# It goes straight up, then curves towards the boss.

# Revised Head Strategy:
# 1. Rectangular block.
# 2. Fillet the top front edge to create the curve.
head = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length)
    .center(0, -5) # Offset slightly back relative to shaft center
    .box(head_width, head_depth, head_height, centered=(True, True, False))
)

# Apply the curve to the front-top edge
# Select the edge at the top (>Z) and front (>Y)
head = head.edges(">Z and >Y").fillet(10.0)

# 4. The Boss (Button)
# Located on the curved face.
# We need to find the face or just position it manually.
# Since we filleted, the face is a bit complex. Let's just place a cylinder.
# We position it on the front face, angled slightly if the fillet was huge, 
# but it looks horizontal in the image.
boss_center_z = shaft_length + (head_height / 2)
# Determine Y position: calculate based on box depth and offset
boss_y_pos = (head_depth / 2) - 5 + boss_length/2 # Approximate surface location

boss = (
    cq.Workplane("XZ")
    .workplane(offset=10) # Initial offset, will move
    .circle(boss_diam / 2)
    .extrude(boss_length)
)
# Rotate and move boss into position
boss = boss.rotate((0,0,0), (1,0,0), -90) # Point along +Y
boss = boss.translate((0, (head_depth/2) - 5, boss_center_z - 5)) 
# Adjust boss position to emerge from the fillet area
# The fillet radius was 10. The box top is at shaft_length + head_height.
# Let's move it down a bit so it's on the vertical part or just starting the curve.

# 5. The Back Mount (The detailed part on the left of the image)
# It looks like a rail mount or a clip mechanism.
# It's attached to the back (-Y) face of the head.
mount = (
    cq.Workplane("XZ")
    .workplane(offset=-(head_depth/2) - 5 - mount_thickness) # Position behind the head
    .rect(head_width, mount_height)
    .extrude(mount_thickness)
)
# Move mount to correct Z height
mount = mount.translate((0, 0, shaft_length + head_height/2))

# Add some detail to the mount (grooves) to make it look like the image
groove = (
    cq.Workplane("YZ")
    .workplane(offset=head_width/2)
    .moveTo(-(head_depth/2) - 5 - mount_thickness/2, shaft_length + head_height/2)
    .rect(mount_thickness + 2, rail_groove_width)
    .extrude(head_width, combine=False)
)
# Cut grooves
mount = mount.cut(groove)

# There is a small connector block between the main head and the mount plate
connector = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length + 5)
    .center(0, -head_depth/2 - 5 - 2.5) # Between head and mount
    .box(head_width * 0.6, 5.0, mount_height * 0.8, centered=(True, True, False))
)


# --- Combine Everything ---
# Using union to fuse parts
result = shaft.union(head).union(boss).union(mount).union(connector)

# Add fillets to smooth transitions (optional but makes it look realistic)
try:
    # Fillet the junction between shaft and head
    result = result.faces(cq.NearestToPointSelector((0, 0, shaft_length))).fillet(2.0)
except:
    pass

# Refine the boss position slightly based on visual check of code logic
# The previous boss was just a standalone object, let's make sure it fuses well.
# It was unioned, so it should be fine.

# Final cleanup of the mount shape to match the "T-slot" look in the back
# The image shows a complex profile. Let's add a vertical slot cut to the mount.
slot_cutter = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length)
    .center(0, -head_depth/2 - 5 - mount_thickness)
    .rect(5, 10) # Small vertical slot profile
    .extrude(head_height)
)
result = result.cut(slot_cutter)

# Export or Render
# show_object(result)