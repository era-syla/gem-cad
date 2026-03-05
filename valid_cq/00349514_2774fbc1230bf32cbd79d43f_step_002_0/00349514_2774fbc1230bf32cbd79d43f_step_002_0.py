import cadquery as cq

# Define parametric dimensions based on the visual proportions of the image
length = 100.0  # Long dimension
height = 12.0   # Vertical dimension
thickness = 2.0 # Thin dimension

# Create the solid rectangular bar geometry
# We create a box centered on the origin.
# - The first argument corresponds to the dimension along the Workplane's x-axis.
# - The second argument corresponds to the dimension along the Workplane's y-axis.
# - The third argument corresponds to the extrusion height (z-axis).
result = cq.Workplane("XY").box(length, thickness, height)