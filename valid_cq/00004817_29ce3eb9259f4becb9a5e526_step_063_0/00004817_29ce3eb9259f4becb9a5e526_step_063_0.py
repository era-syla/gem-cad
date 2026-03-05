import cadquery as cq

# --- Parameters ---
# Rail (Bottom Left)
rail_length = 200.0
rail_width = 20.0
rail_height = 10.0
slot_width = 6.0
slot_depth = 5.0

# Wall (Middle Right)
wall_width = 80.0
wall_thickness = 8.0
num_layers = 4
layer_height = 30.0
v_drop = 15.0  # Depth of the V shape
wall_pos_x = 100.0  # Position along the rail direction
wall_pos_y = 70.0   # Offset from rail

# Small Block (Bottom Right)
block_length = 30.0
block_width = 15.0
block_height = 8.0
block_pos_x = 120.0
block_pos_y = 20.0

# --- Geometry Generation ---

# 1. Generate the Rail
# Profile on YZ plane, extruded along X axis
rail_profile = (
    cq.Workplane("YZ")
    .moveTo(-rail_width / 2, 0)
    .lineTo(rail_width / 2, 0)              # Bottom
    .lineTo(rail_width / 2, rail_height)    # Right Side
    .lineTo(slot_width / 2, rail_height)    # Top Right
    .lineTo(slot_width / 2, rail_height - slot_depth)   # Slot Down
    .lineTo(-slot_width / 2, rail_height - slot_depth)  # Slot Bottom
    .lineTo(-slot_width / 2, rail_height)   # Slot Up
    .lineTo(-rail_width / 2, rail_height)   # Top Left
    .close()
)
rail = rail_profile.extrude(rail_length)

# 2. Generate the Chevron Wall
# Constructed as stacked V-shaped layers to match the image lines
wall_parts = []
# Create a workplane for the wall, offset in X and centered in Y relative to the wall's position
wp_wall = cq.Workplane("YZ").workplane(offset=wall_pos_x).center(wall_pos_y, 0)

for i in range(num_layers):
    bottom_z = i * layer_height
    top_z = (i + 1) * layer_height
    
    pts = []
    
    # Define Bottom Edge of the layer
    if i == 0:
        # Base layer has a flat bottom
        pts.append((-wall_width / 2, 0))
        pts.append((wall_width / 2, 0))
    else:
        # Upper layers have a V-shaped bottom (nesting on the one below)
        pts.append((-wall_width / 2, bottom_z))
        pts.append((0, bottom_z - v_drop))
        pts.append((wall_width / 2, bottom_z))
    
    # Define Top Edge of the layer (V-shaped)
    pts.append((wall_width / 2, top_z))
    pts.append((0, top_z - v_drop))
    pts.append((-wall_width / 2, top_z))
    
    # Create the solid for this layer
    layer = wp_wall.polyline(pts).close().extrude(wall_thickness)
    wall_parts.append(layer)

# Combine all wall layers into one object
wall = wall_parts[0]
for part in wall_parts[1:]:
    wall = wall.union(part)

# 3. Generate the Small Block
block = (
    cq.Workplane("XY")
    .box(block_length, block_width, block_height)
    .translate((block_pos_x, block_pos_y, block_height / 2))
)

# --- Final Result ---
# Combine all parts into a single result variable
result = rail.union(wall).union(block)