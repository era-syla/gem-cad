import cadquery as cq
import math

# --- Parameters ---
length = 220.0
outer_radius = 60.0
thickness = 4.0
arc_angle = 80.0             # Total angle of the curve section
rib_width = 6.0
gap_width = 8.0
rail_width = 10.0            # Width of the solid side rails (projected)
block_len = 18.0
block_width = 12.0
block_height = 8.0           # Height of block above the inner surface
pin_diam = 4.0
pin_height = 4.0

# --- Derived Geometry ---
inner_radius = outer_radius - thickness
half_angle_rad = math.radians(arc_angle / 2.0)
y_max = outer_radius * math.sin(half_angle_rad)

# --- 1. Create the Main Trough Body ---
# Define points for the YZ profile (Arc segment)
# Curvature center is at (0,0), trough hangs in -Z
p_out_start = (y_max, -outer_radius * math.cos(half_angle_rad))
p_out_mid = (0, -outer_radius)
p_out_end = (-y_max, -outer_radius * math.cos(half_angle_rad))

p_in_start = (inner_radius * math.sin(half_angle_rad), -inner_radius * math.cos(half_angle_rad))
p_in_mid = (0, -inner_radius)
p_in_end = (-inner_radius * math.sin(half_angle_rad), -inner_radius * math.cos(half_angle_rad))

# Sketch and Extrude
trough = (
    cq.Workplane("YZ")
    .moveTo(*p_out_start)
    .threePointArc(p_out_mid, p_out_end)
    .lineTo(*p_in_end)
    .threePointArc(p_in_mid, p_in_start)
    .close()
    .extrude(length)
    .translate((-length/2, 0, 0)) # Center the part in X
)

# --- 2. Create Mounting Blocks and Pins ---
# We create a generic block assembly and union it at 6 locations

# Calculate position and height
block_y_center = y_max - block_width/2.0
# Z height of the inner surface at the block's Y center
z_surf_at_block = -math.sqrt(inner_radius**2 - block_y_center**2)
block_top_z = z_surf_at_block + block_height

# Create the base block shape
# Height includes extra to penetrate the rail (trimmed later)
base_block_height = block_height + thickness + 10.0 
block_geo = (
    cq.Workplane("XY")
    .box(block_len, block_width, base_block_height)
    .translate((0, block_y_center, block_top_z - base_block_height/2.0))
)

# Create the Pin
pin_geo = (
    cq.Workplane("XY")
    .circle(pin_diam/2.0)
    .extrude(pin_height)
    .translate((0, block_y_center, block_top_z))
)

# Union Pin to Block and chamfer inner top edge for aesthetics
block_geo = block_geo.union(pin_geo)
# Attempt to chamfer inner edge: Edge at >Z (top of block) and <Y (inner face)
# Note: This selector applies to the block in its positive Y position
try:
    block_geo = block_geo.edges(cq.selectors.BoxSelector(
        (-block_len/2, block_y_center - block_width/2, block_top_z - 1),
        (block_len/2, block_y_center - block_width/2, block_top_z + 1)
    )).chamfer(2.0)
except:
    pass # Skip chamfer if selection fails robustly

# Union blocks to main body
# Locations along X: Start, Middle, End
x_locs = [-length/2 + block_len/2, 0, length/2 - block_len/2]

result_with_blocks = trough
for x in x_locs:
    # Right side block (+Y)
    b_right = block_geo.translate((x, 0, 0))
    result_with_blocks = result_with_blocks.union(b_right)
    
    # Left side block (-Y) - Mirror across XZ plane
    b_left = block_geo.mirror("XZ").translate((x, 0, 0))
    result_with_blocks = result_with_blocks.union(b_left)

# --- 3. Trim Blocks to Outer Curvature ---
# The blocks penetrate through the trough. We trim the bottom to match the outer radius.
limit_cylinder = (
    cq.Workplane("YZ")
    .circle(outer_radius)
    .extrude(length + 20)
    .translate((-length/2 - 10, 0, 0))
)
# Intersect keeps material common to both (i.e., inside the outer radius)
result_trimmed = result_with_blocks.intersect(limit_cylinder)

# --- 4. Cut Slots (Ribs) ---
# Calculate slot dimensions
cut_y_len = (y_max - rail_width) * 2.0 # Span between rails

# Calculate slot layout (two zones to skip middle block area)
# Left Zone
zone_start_x = -length/2 + block_len
zone_end_x = -block_len/2 - rib_width
zone_len = zone_end_x - zone_start_x
pitch = rib_width + gap_width
num_slots = int(zone_len / pitch)

# Build the 2D sketch for all cuts
slot_sketch = cq.Workplane("XY")

def add_slots_to_sketch(sketch, start_x, count):
    for i in range(count):
        cx = start_x + gap_width/2.0 + i*pitch
        sketch = sketch.center(cx, 0).rect(gap_width, cut_y_len).center(-cx, 0)
    return sketch

# Add Left Zone slots
slot_sketch = add_slots_to_sketch(slot_sketch, zone_start_x, num_slots)

# Add Right Zone slots (symmetric start relative to center)
right_zone_start = block_len/2 + rib_width
slot_sketch = add_slots_to_sketch(slot_sketch, right_zone_start, num_slots)

# Perform the Cut
# Cut vertically through the entire depth
final_result = result_trimmed.cut(slot_sketch.extrude(outer_radius*2, both=True))

# Set the result variable
result = final_result