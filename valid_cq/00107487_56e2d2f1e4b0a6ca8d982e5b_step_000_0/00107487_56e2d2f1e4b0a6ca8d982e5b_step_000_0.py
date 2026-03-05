import cadquery as cq

# --- Parameters ---
# Shaft (Rod) dimensions
shaft_length = 150.0
shaft_diameter = 6.0

# Central Block (Carriage/Housing connection) dimensions
block_length = 16.0
block_width = 14.0
block_height = 14.0

# Rail (Housing) dimensions
rail_length = 160.0
rail_width = 12.0
rail_height = 12.0
rail_wall_thickness = 1.5
slot_width = 4.0

# --- Modeling ---

# 1. Create the Shaft (Left side)
# We start slightly inside the block to ensure a valid union
shaft = (
    cq.Workplane("YZ")
    .workplane(offset=2.0) 
    .circle(shaft_diameter / 2.0)
    .extrude(-(shaft_length + 2.0))
)

# Add a small detail tip at the end of the shaft
shaft_tip = (
    cq.Workplane("YZ")
    .workplane(offset=-shaft_length)
    .circle(shaft_diameter / 2.0 - 0.5)
    .extrude(-2.0)
)
shaft = shaft.union(shaft_tip)

# 2. Create the Central Block
# Centered on the intersection of shaft and rail
block = (
    cq.Workplane("YZ")
    .workplane(offset=-block_length / 2.0)
    .rect(block_width, block_height)
    .extrude(block_length)
)

# Add chamfers to the block edges for aesthetics
block = block.edges("|X").chamfer(1.0)
block = block.edges("Z").chamfer(0.5)

# 3. Create the Rail Housing (Right side)
# Extruded profile with a hollow center and a top slot
rail_start_plane = block_length / 2.0

# Create the main rectangular body
rail_body = (
    cq.Workplane("YZ")
    .workplane(offset=rail_start_plane)
    .rect(rail_width, rail_height)
    .extrude(rail_length)
)

# Create the hollow internal volume
rail_inner_cut = (
    cq.Workplane("YZ")
    .workplane(offset=rail_start_plane)
    .rect(rail_width - 2 * rail_wall_thickness, rail_height - 2 * rail_wall_thickness)
    .extrude(rail_length)
)

# Create the slot cut along the top face
rail_slot_cut = (
    cq.Workplane("XY")
    .workplane(offset=rail_height / 2.0)
    .center(rail_start_plane + rail_length / 2.0, 0)
    .rect(rail_length, slot_width)
    .extrude(-rail_wall_thickness * 1.5)
)

# Create mounting holes detail at the far end of the rail
hole_distance_from_end = 8.0
hole_center_x = rail_start_plane + rail_length - hole_distance_from_end

rail_end_hole = (
    cq.Workplane("XZ")
    .workplane(offset=rail_width / 2.0 + 1.0)
    .moveTo(hole_center_x, 0)
    .circle(1.6)
    .extrude(-(rail_width + 2.0))
)

# Apply cuts to the rail body
rail = rail_body.cut(rail_inner_cut).cut(rail_slot_cut).cut(rail_end_hole)

# --- Assembly ---
# Combine all parts into a single object
result = shaft.union(block).union(rail)