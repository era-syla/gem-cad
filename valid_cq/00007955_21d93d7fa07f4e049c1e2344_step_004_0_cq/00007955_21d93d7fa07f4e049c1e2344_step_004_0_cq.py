import cadquery as cq

# Parametric dimensions
plate_width = 100.0  # Width of the plate (X axis)
plate_length = 100.0 # Length of the plate (Y axis)
plate_thickness = 5.0 # Thickness of the plate (Z axis)
corner_radius = 10.0  # Radius of the rounded corners

center_hole_diameter = 10.0 # Diameter of the central hole

mounting_hole_diameter = 6.0 # Diameter of the corner holes
hole_inset_x = 15.0 # Distance from edge to hole center in X
hole_inset_y = 15.0 # Distance from edge to hole center in Y

# Calculate hole positions relative to center
# The hole grid is centered, so we define the offset from the center
x_offset = (plate_width / 2.0) - hole_inset_x
y_offset = (plate_length / 2.0) - hole_inset_y

# Create the base plate with rounded corners
# We start with a rectangle, extrude it, and fillet the Z-parallel edges
result = (
    cq.Workplane("XY")
    .rect(plate_width, plate_length)
    .extrude(plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# Add the central hole
result = (
    result.faces(">Z")
    .workplane()
    .hole(center_hole_diameter)
)

# Add the 4 corner mounting holes
# We use rect to create a grid of points, then cut holes at those points
result = (
    result.faces(">Z")
    .workplane()
    .rect(2 * x_offset, 2 * y_offset, forConstruction=True)
    .vertices()
    .hole(mounting_hole_diameter)
)