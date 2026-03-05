import cadquery as cq

# Define parameters for the plate and hole pattern
plate_length = 100.0   # Dimension along X
plate_width = 100.0    # Dimension along Y
plate_thickness = 10.0 # Thickness of the plate

# Hole configuration
hole_diameter = 3.0
hole_depth = 5.0  # Depth of the holes (blind holes)

# Pattern definition
# Based on the image, the holes are arranged in a pattern.
# It looks like two parallel lines of holes, but slightly staggered or angled.
# However, a closer look suggests a hexagonal or triangular grid layout, or simply two rows.
# Let's assume a symmetric layout of two rows of 3 holes.
# The holes appear to be centered on the plate.

# Let's define the positions relative to the center.
# The pattern looks like a 2x3 grid, but the middle row is shifted? 
# No, looking closely at the image:
# There are two rows. Let's call them Row A and Row B.
# Row A has 3 holes. Row B has 3 holes.
# They are parallel.
# Let's assume a standard rectangular pattern for simplicity, centered on the face.
# Alternatively, it could be a specific bolt pattern. 
# Without specific dimensions, I will create a parametric grid.

num_rows = 2
num_cols = 3
row_spacing = 20.0
col_spacing = 20.0

# Create the base plate
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# Create the list of points for the holes
# The image shows 6 holes. They look like they are in a staggered pattern or just a tilted view of a rectangular grid.
# Let's try to match the visual arrangement. It looks like a 2x3 grid rotated 45 degrees relative to the view, 
# or simply aligned with the plate axes. Let's assume alignment with plate axes (X and Y).
# The holes are in the center region.

# Let's define points for a 2x3 grid centered at (0,0)
# positions = []
# for r in range(num_rows):
#     y = (r - (num_rows - 1) / 2) * row_spacing
#     for c in range(num_cols):
#         x = (c - (num_cols - 1) / 2) * col_spacing
#         positions.append((x, y))

# Let's refine the pattern to match the "feel" of the image. 
# The holes form a tight group in the middle.
# Let's use pushPoints with a rectangular grid.

result = (
    result
    .faces(">Z")
    .workplane()
    .rarray(
        xSpacing=20,  # Spacing between columns
        ySpacing=15,  # Spacing between rows
        xCount=3,     # 3 columns
        yCount=2,     # 2 rows
        center=True   # Centered on the face
    )
    .hole(hole_diameter, depth=hole_depth)
)

# If the holes are through-holes, remove the depth argument or set it > plate_thickness
# The image shows dark bottoms, implying blind holes or shadows. Blind is safer without more info.
# I'll stick with blind holes as defined by hole_depth.