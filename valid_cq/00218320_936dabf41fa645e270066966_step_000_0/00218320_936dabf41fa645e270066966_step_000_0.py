import cadquery as cq

# -- Parameters --
# Adjust dimensions to match the proportions in the image
width = 200.0         # Horizontal length
height_right = 150.0  # Height of the right vertical leg
height_left = 60.0    # Height of the left vertical leg
extension_len = 20.0  # Length of the small top extension
tube_radius = 4.0     # Radius of the pipe

# -- Geometry Construction --

# 1. Define the path for the main trapezoidal loop
# We sketch on the XZ plane (Front view)
# Path starts at origin (0,0,0) -> Bottom Left
path_loop = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(width, 0)              # Bottom edge to bottom-right
    .lineTo(width, height_right)   # Right edge to top-right
    .lineTo(0, height_left)        # Top diagonal edge to top-left
    .close()                       # Close back to (0,0)
)

# 2. Sweep the main loop
# The path starts at (0,0) and moves along the X-axis.
# We define the circular profile on the YZ plane (perpendicular to start).
solid_loop = (
    cq.Workplane("YZ")
    .circle(tube_radius)
    .sweep(path_loop)
)

# 3. Define the path for the vertical extension
# Starts at the top-right corner and goes upwards
path_extension = (
    cq.Workplane("XZ")
    .moveTo(width, height_right)
    .lineTo(width, height_right + extension_len)
)

# 4. Sweep the extension
# The path starts at (width, 0, height_right) and moves in +Z.
# We define the circular profile on the XY plane (perpendicular to Z),
# offset to the correct height and moved to the correct X position.
solid_extension = (
    cq.Workplane("XY")
    .workplane(offset=height_right)
    .moveTo(width, 0)
    .circle(tube_radius)
    .sweep(path_extension)
)

# 5. Combine the geometries
result = solid_loop.union(solid_extension)

# Export or display (for local usage context, usually not included in strict code generation unless requested)
# cq.exporters.export(result, "model.step")