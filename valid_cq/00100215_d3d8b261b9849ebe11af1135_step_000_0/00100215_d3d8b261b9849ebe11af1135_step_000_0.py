import cadquery as cq

# Parametric dimensions for the 3D model
# Main (longer) rectangular bar dimensions
length_main = 100.0
width_main = 30.0
thickness = 8.0

# Secondary (smaller) rectangular block dimensions
length_small = 35.0
width_small = 25.0

# Positioning parameters
gap = 15.0          # Distance between the two blocks
x_offset = -25.0    # Shift of the small block relative to the center of the main block

# Calculate Y-axis offset to position the small block with the specified gap
# Distance is sum of half-widths plus the gap
y_pos = (width_main / 2.0) + gap + (width_small / 2.0)

# Create the main bar centered at the origin
main_bar = cq.Workplane("XY").box(length_main, width_main, thickness)

# Create the small block offset in X and Y
small_block = (
    cq.Workplane("XY")
    .center(x_offset, y_pos)
    .box(length_small, width_small, thickness)
)

# Combine the two disjoint solids into a single compound object
result = main_bar.union(small_block)