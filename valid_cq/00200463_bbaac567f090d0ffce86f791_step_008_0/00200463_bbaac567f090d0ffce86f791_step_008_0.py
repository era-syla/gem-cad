import cadquery as cq

# Parametric dimensions based on visual estimation of the image
length = 100.0     # Long dimension
height = 25.0      # Vertical dimension
thickness = 2.0    # Depth/Thickness dimension

# Create the solid geometry
# We create a box centered at the origin.
# To match the "standing" orientation seen in the image (assuming Z is up),
# we map:
#   - X axis: Length
#   - Y axis: Thickness
#   - Z axis: Height
result = cq.Workplane("XY").box(length, thickness, height)