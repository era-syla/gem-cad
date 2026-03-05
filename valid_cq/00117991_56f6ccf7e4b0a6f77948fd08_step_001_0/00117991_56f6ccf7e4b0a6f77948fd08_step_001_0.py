import cadquery as cq

# --- Parameters ---

# Wheel parameters
wheel_rim_od = 60.0
wheel_rim_id = 54.0
wheel_height = 5.0
hub_od = 10.0
hub_id = 4.0
spoke_length = 95.0
spoke_width = 4.0

# Clip parameters
clip_width = 14.0
clip_depth = 8.0
clip_height = 7.0
clip_wall_thickness = 2.0

# Cube parameters
cube_size = 30.0

# --- Geometry Construction ---

# 1. Create the Spoked Wheel
# Rim
rim = (
    cq.Workplane("XY")
    .circle(wheel_rim_od / 2.0)
    .circle(wheel_rim_id / 2.0)
    .extrude(wheel_height)
)

# Central Hub
hub = (
    cq.Workplane("XY")
    .circle(hub_od / 2.0)
    .circle(hub_id / 2.0)
    .extrude(wheel_height)
)

# Spokes (3 bars rotated to form 6 spokes)
spoke_base = cq.Workplane("XY").box(spoke_length, spoke_width, wheel_height)
spokes = spoke_base.union(spoke_base.rotate((0, 0, 0), (0, 0, 1), 60))
spokes = spokes.union(spoke_base.rotate((0, 0, 0), (0, 0, 1), 120))

# Combine wheel parts
wheel = rim.union(hub).union(spokes)


# 2. Create the Clip (E-shaped channel)
# Base block centered at origin
clip_block = cq.Workplane("XY").box(clip_width, clip_depth, clip_height)

# Calculate slot dimensions
slot_width = (clip_width - (3 * clip_wall_thickness)) / 2.0
slot_cut_height = clip_height - clip_wall_thickness

# Calculate Z position for the cut (cutting from the bottom up)
# Block bottom is at -clip_height/2
# Cutter center needs to be at bottom + cutter_height/2
cut_z_center = -(clip_height / 2.0) + (slot_cut_height / 2.0)

# Calculate X positions for the two slots
# Right slot center: (Width/2) - Wall - (Slot/2)
slot_x_offset = (clip_width / 2.0) - clip_wall_thickness - (slot_width / 2.0)

# Create cutters
cutter_right = (
    cq.Workplane("XY")
    .box(slot_width, clip_depth, slot_cut_height)
    .translate((slot_x_offset, 0, cut_z_center))
)
cutter_left = (
    cq.Workplane("XY")
    .box(slot_width, clip_depth, slot_cut_height)
    .translate((-slot_x_offset, 0, cut_z_center))
)

# Apply cuts and position the clip
clip = clip_block.cut(cutter_left).cut(cutter_right)
# Move clip to position (approx (50, 50) relative to wheel) and sit on ground
clip = clip.translate((50, 50, clip_height / 2.0))


# 3. Create the Cube
cube = cq.Workplane("XY").box(cube_size, cube_size, cube_size)
# Move cube to position (approx (90, 40)) and sit on ground
cube = cube.translate((90, 40, cube_size / 2.0))


# --- Final Assembly ---
result = wheel.union(clip).union(cube)