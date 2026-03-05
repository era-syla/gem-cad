import cadquery as cq

# Parametric dimensions
height = 80.0
width = 8.0
depth_thick = 8.0
depth_thin = 1.5
chamfer_size = 2.5
spacing = 25.0

# --- Create Left Object (Thick bar with corner chamfer) ---

# Base solid: Rectangular prism
left_bar = cq.Workplane("XY").box(width, depth_thick, height, centered=(True, True, False))

# Create a cutting tool to remove the corner
# The cutter is a pyramid shape created by lofting a triangle on top to a point inside
x_corner = width / 2.0
y_corner = depth_thick / 2.0

cutter = (
    cq.Workplane("XY")
    .workplane(offset=height)
    .moveTo(x_corner, y_corner)
    .lineTo(x_corner - chamfer_size, y_corner)
    .lineTo(x_corner, y_corner - chamfer_size)
    .close()  # Triangular base on top face
    .workplane(offset=-chamfer_size)
    .moveTo(x_corner, y_corner)
    .rect(0.001, 0.001)  # Approximate point tip inside the block
    .loft()
)

# Apply the cut
left_bar = left_bar.cut(cutter)


# --- Create Right Object (Thin strip) ---

right_bar = cq.Workplane("XY").box(width, depth_thin, height, centered=(True, True, False))


# --- Assembly and Positioning ---

# Position the left bar to the left side
final_left = left_bar.translate((-spacing / 2.0, 0, 0))

# Position the right bar to the right side
final_right = right_bar.translate((spacing / 2.0, 0, 0))

# Combine into a single compound object
result = final_left.union(final_right)