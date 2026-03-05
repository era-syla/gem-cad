import cadquery as cq

# --- Dimensions ---

# Rail dimensions
rail_length = 200.0
rail_width = 20.0
rail_height = 10.0
slot_width = 6.0
slot_depth = 4.0

# V-Block / Backstop dimensions
backstop_width = 10.0  # Thickness
backstop_base_width = 60.0 # Total width at bottom
backstop_short_height = 40.0
backstop_tall_height = 80.0
notch_center_height = 30.0 # Height of the bottom of the V-notch
notch_center_x = 0.0 # Centered on the block

# Small block dimensions
block_length = 30.0
block_width = 20.0
block_height = 10.0

# Positioning
backstop_offset_x = 50.0
backstop_offset_y = 50.0
block_offset_x = 80.0
block_offset_y = 50.0
block_offset_z = 0.0

# --- Modeling ---

# 1. Create the slotted rail
rail = (
    cq.Workplane("XY")
    .box(rail_length, rail_width, rail_height)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rail_length, slot_width)
    .cutBlind(-slot_depth)
)

# 2. Create the V-notched plate/backstop
# We sketch the profile on the YZ plane (vertical) and extrude in X
backstop_pts = [
    (0, 0),
    (backstop_base_width, 0),
    (backstop_base_width, backstop_tall_height), # Tall side
    (backstop_base_width/2, notch_center_height + 20), # The V notch dip
    (0, backstop_short_height), # Short side
    (0,0) # Close loop
]

# Let's redefine points relative to a center for easier symmetry if needed, 
# but looking at the image, one side is taller.
# Let's approximate the shape from the image:
# It looks like a vertical plate with a V cut out of the top.
# Left height: ~40, Right height: ~70, Center dip: ~30. Width: ~60. Thickness ~5.
bs_w = 60.0
bs_h_left = 50.0
bs_h_right = 80.0
bs_v_bottom = 40.0
bs_thick = 5.0

backstop = (
    cq.Workplane("XY")
    .workplane(offset=0) # Start on ground
    .moveTo(-bs_w/2, 0)
    .lineTo(bs_w/2, 0)
    .lineTo(bs_w/2, bs_h_right)
    .lineTo(0, bs_v_bottom)
    .lineTo(-bs_w/2, bs_h_left)
    .close()
    .extrude(bs_thick)
    # Rotate it to stand up
    .rotate((0,0,0), (1,0,0), 90)
    # Move it into position relative to rail
    .translate((50, 80, 0)) 
)


# 3. Create the small block
small_block = (
    cq.Workplane("XY")
    .box(block_length, block_width, block_height)
    .translate((60, 40, block_height/2))
)

# Combine all parts into one result for visualization
# The rail is centered at (0,0,0) by default box behavior (center=True)
# We need to shift the rail up so Z=0 is the bottom
rail = rail.translate((0, 0, rail_height/2))

result = rail.union(backstop).union(small_block)