import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions roughly approximating a phone (e.g., iPhone 5/SE style)
phone_length = 125.0
phone_width = 60.0
phone_thickness = 8.0

# Case wall settings
wall_thickness = 2.0
bottom_thickness = 1.5
corner_radius = 10.0  # External corner radius

# Bumper lip settings (the small overhang to hold the screen)
lip_overhang = 1.0
lip_height = 0.8

# Cutout dimensions (approximate)
# Side cutout (e.g., for volume/mute buttons)
side_cutout_length = 35.0
side_cutout_height = 6.0 # From top edge down
side_cutout_offset = 15.0 # From top left corner

# Bottom cutout (e.g., for charging/speakers)
bottom_cutout_width = 30.0
bottom_cutout_depth = 5.0 # How much of the bottom edge is removed

# --- Geometry Construction ---

# 1. Base Shape: The main block
# Create a rounded rectangle for the outer boundary
outer_profile = (
    cq.Workplane("XY")
    .rect(phone_length + 2*wall_thickness, phone_width + 2*wall_thickness)
    .extrude(phone_thickness + bottom_thickness + lip_height)
)

# Apply fillets to the four vertical corners
outer_shell = outer_profile.edges("|Z").fillet(corner_radius)

# 2. Hollow out the inside to create the main cavity
# We need to subtract the phone's volume + clearance from the block
# The cavity starts *above* the bottom_thickness
cavity = (
    cq.Workplane("XY")
    .workplane(offset=bottom_thickness)
    .rect(phone_length, phone_width)
    .extrude(phone_thickness + lip_height + 10) # Overshoot the top
)

# Fillet the cavity corners to match the outer shape but smaller
inner_radius = corner_radius - wall_thickness
cavity = cavity.edges("|Z").fillet(inner_radius)

# Create the initial cup shape
main_body = outer_shell.cut(cavity)

# 3. Create the Overhanging Lip
# The image shows a small lip at the very top edge to retain the phone.
# We create this by making a shell cut that is slightly undercut.
# A simple way in constructive geometry:
# The cavity we just cut was straight vertical.
# The 'lip' is actually material that *wasn't* cut.
# However, the cavity method above creates straight walls. 
# Let's recreate the lip by adding a rim or defining the cut differently.

# Better approach for lip:
# We have a 'main_body'. We need to cut away the top opening which is slightly smaller
# than the internal cavity.
# Actually, the previous step cut the *full* phone width.
# To make a lip, we should have cut a smaller rectangle at the very top, or added material back.
# Let's use the 'add material' strategy.
# Create a frame at the top.

lip_shape = (
    cq.Workplane("XY")
    .workplane(offset=bottom_thickness + phone_thickness)
    .rect(phone_length + 2*wall_thickness, phone_width + 2*wall_thickness)
    .rect(phone_length - 2*lip_overhang, phone_width - 2*lip_overhang) # The opening
    .extrude(lip_height)
)
# Apply fillets to the lip
lip_shape = lip_shape.edges("|Z").fillet(corner_radius)

# Note: In the image, the lip seems integral. 
# Let's refine the Cut strategy. 
# We'll stick with `main_body` as defined (which holds the full phone), 
# and assume the "lip" is actually just the top edge, and perhaps the phone snaps in.
# BUT, looking closely at the top-left inner corner of the image, there is an undercut.
# Let's add the lip geometry to the top of the walls.
# Actually, the simplest way to match the image is to add the inward protrusion.

# Let's create the lip protrusion on the inside top edge
lip_profile = (
    cq.Workplane("XY")
    .workplane(offset=bottom_thickness + phone_thickness)
    .rect(phone_length, phone_width) # Outer boundary of the lip addition (matches inner wall)
    .rect(phone_length - 2*lip_overhang, phone_width - 2*lip_overhang) # Inner opening
    .extrude(lip_height)
)
# Fillet the lip profile to match the inner curvature
lip_profile = lip_profile.edges("|Z").fillet(inner_radius)

# Fuse the lip to the body
result_shape = main_body.union(lip_profile)


# 4. Cutouts

# Left Side Cutout (Volume/Mute)
# We need to cut through the left wall.
# Coordinate system: X is length, Y is width. Left wall is at -Y/2 roughly? 
# No, rectangular origin is center.
# Left side wall corresponds to Y = +width/2 or -width/2. 
# Let's assume standard orientation: X is long axis, Y is short axis.
# The image shows a cutout on the long side (the "top" in the image perspective, let's call this +Y).

# Create a cutting tool for the side
side_cutter = (
    cq.Workplane("XZ") # Orientation for side cut
    .workplane(offset=phone_width/2 + wall_thickness + 1) # Position outside the case
    .moveTo(-phone_length/2 + side_cutout_offset + side_cutout_length/2, bottom_thickness + phone_thickness)
    .rect(side_cutout_length, side_cutout_height * 4) # Make it tall enough to cut down
    .extrude(-wall_thickness * 3) # Cut inward
)

result_shape = result_shape.cut(side_cutter)


# Bottom Cutout (Charging port area)
# This looks like a large section of the wall is removed on one of the short ends.
# In the image, it's the right-hand side (positive X).

bottom_cutter = (
    cq.Workplane("YZ")
    .workplane(offset=phone_length/2 + wall_thickness + 1)
    .moveTo(0, bottom_thickness + phone_thickness/2) # Center of the face
    .rect(bottom_cutout_width, phone_thickness * 2) # Tall rectangle
    .extrude(-wall_thickness * 3)
)

result_shape = result_shape.cut(bottom_cutter)

# Top Cutout (Headphone jack / Power button)
# The image shows a small cutout on the far left short edge (Negative X).
top_cutout_width = 10.0
top_cutter = (
    cq.Workplane("YZ")
    .workplane(offset=-(phone_length/2 + wall_thickness + 1))
    .moveTo(phone_width/4, bottom_thickness + phone_thickness) # Offset slightly
    .rect(top_cutout_width, 5.0)
    .extrude(wall_thickness * 3)
)
# Note: The image actually shows the large opening on the right (bottom of phone)
# and a large opening on the left side (volume buttons).
# It also shows a distinct large cutout on the left short edge (top of phone).
# Let's adjust the "Top Cutout" to be larger based on the image's left-most curve.

top_large_cutter = (
     cq.Workplane("YZ")
    .workplane(offset=-(phone_length/2 + wall_thickness + 1))
    .moveTo(0, bottom_thickness + phone_thickness/2 + 2) 
    .rect(phone_width * 0.6, phone_thickness * 2) 
    .extrude(wall_thickness * 3)
)
result_shape = result_shape.cut(top_large_cutter)

# 5. Refining Edges (Chamfers/Fillets)
# The image shows smooth edges on the top lip and the cutouts.

# Fillet external vertical edges (already done)

# Fillet the top edges of the case
try:
    result_shape = result_shape.edges(">Z").fillet(0.5)
except:
    pass # Sometimes fails if geometry is complex, skip if so

# Fillet the bottom external edge
try:
    result_shape = result_shape.edges("<Z").fillet(1.0)
except:
    pass

# Assign to result
result = result_shape