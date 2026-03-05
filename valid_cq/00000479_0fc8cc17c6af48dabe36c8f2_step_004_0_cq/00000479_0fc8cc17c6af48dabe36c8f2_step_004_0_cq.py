import cadquery as cq

# Parameters
diameter = 50.0
height = 50.0
fillet_radius = 5.0

# Create the base cylinder
result = cq.Workplane("XY").circle(diameter / 2.0).extrude(height)

# Apply fillet to the top edge
result = result.faces(">Z").edges().fillet(fillet_radius)