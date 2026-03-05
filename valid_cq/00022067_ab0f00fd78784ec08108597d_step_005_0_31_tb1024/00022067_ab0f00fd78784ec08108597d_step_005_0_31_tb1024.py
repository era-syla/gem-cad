import cadquery as cq

# Parameters
length = 150.0
diameter = 5.0

# Create the solid model (a simple cylindrical rod)
result = cq.Workplane("XY").circle(diameter / 2.0).extrude(length)