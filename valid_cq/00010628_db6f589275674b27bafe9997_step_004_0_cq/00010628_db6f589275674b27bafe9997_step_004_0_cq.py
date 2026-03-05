import cadquery as cq

# Parametric dimensions
# The image shows a long, thin rectangular bar.
# These dimensions are estimates based on the visual proportions.
length = 200.0  # Total length of the bar
width = 5.0     # Width of the rectangular cross-section
thickness = 3.0 # Thickness/height of the rectangular cross-section

# Create the rectangular bar
# We draw a rectangle on the XY plane and extrude it
result = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(thickness)
)

# Alternatively, using the box method for a centered primitive
# result = cq.Workplane("XY").box(length, width, thickness)