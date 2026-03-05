import cadquery as cq

# Parameters for dimensions
length = 120.0
width = 30.0
thickness = 8.0
gap = 5.0          # Gap between the bottom parallel bars
lift = 50.0        # Vertical distance between levels
stagger = 40.0     # Horizontal offset for the floating pieces

# Create a base rectangular bar centered at the origin
# This serves as the template for all four pieces
bar = cq.Workplane("XY").box(length, width, thickness)

# Create the bottom assembly: two parallel bars separated by a gap
# We shift them along the Y-axis (width direction)
bottom_left = bar.translate((0, -(width + gap) / 2, 0))
bottom_right = bar.translate((0, (width + gap) / 2, 0))

# Create the middle floating piece
# Shifted up in Z and to the left (negative X) to match the image perspective
middle_piece = bar.translate((-stagger, 0, lift))

# Create the top floating piece
# Shifted further up in Z and to the right (positive X)
top_piece = bar.translate((stagger, 0, lift * 2))

# Combine all parts into the final result
result = bottom_left.union(bottom_right).union(middle_piece).union(top_piece)