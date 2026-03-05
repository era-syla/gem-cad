import cadquery as cq

# Parametric dimensions
pitch = 10.0            # Distance between hole centers
cols = 5                # Number of columns of holes
rows = 2                # Number of rows of holes
thickness = 3.0         # Plate thickness
hole_diameter = 4.5     # Diameter of the holes
margin = 5.0            # Distance from the hole center to the outer edge
corner_radius = 4.0     # Fillet radius for the corners

# Calculate overall dimensions
length = (cols - 1) * pitch + 2 * margin
width = (rows - 1) * pitch + 2 * margin

# Create the 3D model
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")
    .fillet(corner_radius)
    .faces(">Z")
    .workplane()
    .rarray(pitch, pitch, cols, rows)
    .hole(hole_diameter)
)