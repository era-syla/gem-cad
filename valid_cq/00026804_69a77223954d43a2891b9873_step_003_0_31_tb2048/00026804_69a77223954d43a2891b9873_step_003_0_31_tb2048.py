import cadquery as cq

# Parameters
radius = 5.0
length = 100.0

# Create the solid geometry (a simple cylinder/rod)
result = cq.Workplane("XY").circle(radius).extrude(length)