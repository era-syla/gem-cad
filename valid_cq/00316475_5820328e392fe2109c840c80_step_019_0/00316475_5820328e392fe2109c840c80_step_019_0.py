import cadquery as cq

# Model parameters
diameter = 50.0   # Diameter of the cylinder
thickness = 5.0   # Thickness (height) of the cylinder

# Create the cylindrical disc
# 1. Start a workplane on the XY plane
# 2. Draw a circle with the specified radius (diameter / 2)
# 3. Extrude the circle by the specified thickness
result = cq.Workplane("XY").circle(diameter / 2.0).extrude(thickness)