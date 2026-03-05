import cadquery as cq

# Parametric definitions
cube_size = 50.0  # Overall size of the cube
wall_thickness = 10.0  # Thickness of the frame/walls
hole_size = cube_size - (2 * wall_thickness) # Size of the cutouts

# Create the base solid cube
base = cq.Workplane("XY").box(cube_size, cube_size, cube_size)

# Create the cutouts
# We need to cut a square hole through the X, Y, and Z axes.

# Cut along Z axis
z_cut = (
    cq.Workplane("XY")
    .rect(hole_size, hole_size)
    .extrude(cube_size, both=True)
)

# Cut along Y axis (XZ plane)
y_cut = (
    cq.Workplane("XZ")
    .rect(hole_size, hole_size)
    .extrude(cube_size, both=True)
)

# Cut along X axis (YZ plane)
x_cut = (
    cq.Workplane("YZ")
    .rect(hole_size, hole_size)
    .extrude(cube_size, both=True)
)

# Combine operations
# Start with base, subtract the three cutting shapes
result = (
    base
    .cut(z_cut)
    .cut(y_cut)
    .cut(x_cut)
)