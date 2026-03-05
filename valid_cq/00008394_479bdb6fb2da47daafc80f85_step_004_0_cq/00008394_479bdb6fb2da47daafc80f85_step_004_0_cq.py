import cadquery as cq

# Define parameters for the cylinder
# Dimensions are estimated based on visual proportions
diameter = 50.0
height = 75.0
radius = diameter / 2.0

# Create the cylinder using the Workplane and circle extrude method
# Alternatively, could use cq.Solid.makeCylinder, but the fluent API is more idiomatic
result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(height)
)

# Export the result if needed (e.g., to STL or STEP)
# cq.exporters.export(result, "cylinder.step")