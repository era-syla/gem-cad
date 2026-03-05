import cadquery as cq

# Parametric dimensions
# Long Bar parameters
bar_length = 200.0
bar_width = 20.0
bar_thickness = 5.0
hole_diameter = 8.0
hole_margin = 15.0  # Distance from the edge to the center of the hole

# Small Block parameters
block_side = 25.0  # Appears square
block_thickness = 5.0
block_hole_diameter = 2.0

# Create the Long Bar
# Start with a rectangular box
long_bar = cq.Workplane("XY").box(bar_length, bar_width, bar_thickness)

# Add holes at both ends
# Calculating center points relative to the center of the bar
hole_x_offset = (bar_length / 2) - hole_margin

long_bar = (
    long_bar.faces(">Z")
    .workplane()
    .pushPoints([(-hole_x_offset, 0), (hole_x_offset, 0)])
    .hole(hole_diameter)
)

# Create the Small Block
# Create a separate workplane for the block, offset from the bar for visibility
# (The image shows them as separate objects, likely an assembly or exploded view)
block_offset_y = -50.0 # Move it 'down' relative to the bar in the view

small_block = (
    cq.Workplane("XY")
    .center(0, block_offset_y) # Position relative to origin
    .box(block_side, block_side, block_thickness)
)

# Add the small side hole to the block
# The hole seems to be on one of the side faces (e.g., -Y face), going inwards
small_block = (
    small_block.faces("<Y")
    .workplane()
    .center(0, 0) # Center on the face
    .hole(block_hole_diameter, depth=block_side/2) # Drill halfway through
)

# Combine both parts into a single result for visualization
# Note: In a real assembly, these might be kept separate, but for a single 'result' variable
# representing the image content, we union them.
result = long_bar.union(small_block)

# Export or Display (standard practice requires just defining 'result')