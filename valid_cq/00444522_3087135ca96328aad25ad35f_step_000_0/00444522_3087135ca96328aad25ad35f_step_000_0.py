import cadquery as cq

# --- Parameters ---
# Overall dimensions
rail_length = 300.0

# Rail profile dimensions (approx. MGN12 style)
rail_width = 12.0
rail_depth = 8.0
rail_groove_radius = 1.5

# Carriage block dimensions
block_height = 36.0  # Dimension along the rail (Z)
block_width = 24.0   # Dimension across the rail (X)
block_depth = 16.0   # Thickness (Y)

# Mounting hole configuration
hole_diameter = 2.4
hole_spacing_x = 15.0
hole_spacing_z = 10.0 # Vertical spacing between rows
num_rows = 3
num_cols = 2

# --- Modeling ---

# 1. Create the Rail
# Profile: A rectangle with circular grooves on the sides to simulate linear guide tracks
rail_sketch = (
    cq.Sketch()
    .rect(rail_width, rail_depth)
    .push([(-rail_width/2.0, 0), (rail_width/2.0, 0)])
    .circle(rail_groove_radius, mode='s')
)

rail = (
    cq.Workplane("XY")
    .placeSketch(rail_sketch)
    .extrude(rail_length)
)

# 2. Create the Carriage Block
# Position the block at the top end of the rail.
# The block's Z center is calculated to align its top face with the rail's top face.
block_center_z = rail_length - (block_height / 2.0)

carriage_block = (
    cq.Workplane("XY")
    .workplane(offset=block_center_z)
    .box(block_width, block_depth, block_height)
)

# 3. Add Mounting Holes
# Select the front face (assumed +Y direction) and add the 2x3 grid of holes
carriage_with_holes = (
    carriage_block.faces(">Y")
    .workplane()
    # Note: On the >Y face, local Y axis corresponds to Global Z axis
    .rarray(hole_spacing_x, hole_spacing_z, num_cols, num_rows)
    .hole(hole_diameter)
)

# 4. Final Assembly
# Union the rail and the machined carriage block into one solid
result = rail.union(carriage_with_holes)