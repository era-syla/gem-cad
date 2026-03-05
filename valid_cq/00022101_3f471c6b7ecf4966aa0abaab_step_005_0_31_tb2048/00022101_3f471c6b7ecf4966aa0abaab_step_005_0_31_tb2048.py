import cadquery as cq

# Parameters
diameter = 2.0
length = 150.0

# Create the rod
result = cq.Workplane("XY").circle(diameter / 2.0).extrude(length)