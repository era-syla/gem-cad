import cadquery as cq

# Parametric dimensions
length = 200.0  # Total length of the rod
diameter = 6.0  # Diameter of the rod

# Create the solid cylindrical rod
result = cq.Workplane("XY").circle(diameter / 2.0).extrude(length)