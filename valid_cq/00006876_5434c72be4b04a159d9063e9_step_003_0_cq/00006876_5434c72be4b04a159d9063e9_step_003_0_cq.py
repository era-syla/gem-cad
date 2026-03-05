import cadquery as cq

# Parametric dimensions
diameter = 5.0    # Diameter of the rod
length = 100.0    # Length of the rod

# Create the rod (cylinder)
# We align it along the Z axis, centered at the origin for the base
result = cq.Workplane("XY").circle(diameter / 2).extrude(length)

# Alternatively, a simpler way to create a cylinder directly:
# result = cq.Workplane("XY").cylinder(length, diameter / 2, centered=(True, True, False))

# Export the result if needed
# cq.exporters.export(result, "rod.step")