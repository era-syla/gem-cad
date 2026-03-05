import cadquery as cq

# --- Parametric Dimensions ---
# Section 1: Threaded End (represented as cylinder)
thread_diam = 12.0
thread_len = 15.0

# Section 2: Middle Shoulder
mid_diam = 15.0
mid_len = 35.0

# Section 3: Long Shaft
shaft_diam = 10.0
shaft_len = 45.0

# Feature Dimensions
flat_width = 12.0      # Width across flats (wrench size)
flat_len = 16.0        # Length of the flat section
flat_offset = 2.0      # Offset from the thread shoulder
tip_radius = 4.0       # Fillet radius for the nose

# --- Geometry Construction ---

# 1. Main Shaft Body
# Built sequentially along the Z-axis
result = (
    cq.Workplane("XY")
    # Threaded section
    .circle(thread_diam / 2.0)
    .extrude(thread_len)
    # Middle section (step up)
    .faces(">Z").workplane()
    .circle(mid_diam / 2.0)
    .extrude(mid_len)
    # Shaft section (step down)
    .faces(">Z").workplane()
    .circle(shaft_diam / 2.0)
    .extrude(shaft_len)
)

# 2. Rounded Tip
# Apply a fillet to the top edge to create the bullet-nose shape
result = result.faces(">Z").edges().fillet(tip_radius)

# 3. Wrench Flats
# Create a cutter object to remove material from the sides of the middle section
z_flat_start = thread_len + flat_offset
cut_block_size = mid_diam * 2.0  # Large enough to clear the round
cut_center_y = (flat_width / 2.0) + (cut_block_size / 2.0)

cutter = (
    cq.Workplane("XY")
    .workplane(offset=z_flat_start)
    # Define two rectangles positioned to leave 'flat_width' in the center
    .rect(cut_block_size, cut_block_size)
    .translate((0, cut_center_y))
    .rect(cut_block_size, cut_block_size)
    .translate((0, -cut_center_y))
    .extrude(flat_len)
)

# Subtract the cutter from the main body
result = result.cut(cutter)

# 4. Chamfer thread start
result = result.faces("<Z").edges().chamfer(0.5)