import cadquery as cq

# --- Parametric Dimensions ---
# Central connecting block
block_length = 15.0
block_width = 12.0
block_height = 10.0
block_chamfer = 0.8

# Hexagonal Shaft (Left side)
shaft_length = 135.0
shaft_flat_size = 5.0  # Distance across flats
# Calculate circumscribed diameter for the hexagon (D = d / cos(30))
shaft_outer_dia = shaft_flat_size / 0.866025
shaft_tip_chamfer = 0.5

# Parallel Rails (Right side)
rail_length = 150.0
rail_height = 8.0
rail_thickness = 1.8
rail_gap = 4.5  # Distance between the two rails
rail_hole_diameter = 2.5
rail_hole_offset = 6.0  # Distance from the end of the rail

# --- Geometry Construction ---

# 1. Central Block
# Create the main body centered at the origin
center_block = cq.Workplane("XY").box(block_length, block_width, block_height)
# Apply chamfers to all edges for a machined/molded look
center_block = center_block.edges().chamfer(block_chamfer)

# 2. Hexagonal Shaft
# Create a sketch on the YZ plane offset to the left face of the block
# Extrude in the negative X direction
shaft = (cq.Workplane("YZ")
         .workplane(offset=-block_length / 2.0)
         .polygon(6, shaft_outer_dia)
         .extrude(-shaft_length))

# Add a cosmetic chamfer to the tip of the shaft
shaft = shaft.faces("<X").edges().chamfer(shaft_tip_chamfer)

# 3. Parallel Rails
# Create a sketch on the YZ plane offset to the right face of the block
# The rails are two vertical rectangular bars separated by a gap
rail_center_offset = (rail_gap + rail_thickness) / 2.0

rails = (cq.Workplane("YZ")
         .workplane(offset=block_length / 2.0)
         .pushPoints([(rail_center_offset, 0), (-rail_center_offset, 0)])
         .rect(rail_thickness, rail_height)
         .extrude(rail_length))

# 4. End Feature (Hole)
# Cut a hole through both rails near the tip
hole_x_pos = (block_length / 2.0) + rail_length - rail_hole_offset

# Use a cylinder extruded along the Y axis (width) to cut the hole
hole_cutter = (cq.Workplane("XZ")
               .moveTo(hole_x_pos, 0)
               .circle(rail_hole_diameter / 2.0)
               .extrude(block_width * 2, both=True))

# --- Final Assembly ---
# Union all solid parts and cut the hole
result = center_block.union(shaft).union(rails).cut(hole_cutter)