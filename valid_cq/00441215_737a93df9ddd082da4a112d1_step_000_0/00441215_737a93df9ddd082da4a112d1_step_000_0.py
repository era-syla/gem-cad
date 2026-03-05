import cadquery as cq

# Parametric dimensions
rod_length = 300.0
rod_diameter = 6.0

# Create the solid cylindrical rod
# We start on the XY plane, draw the circular cross-section, and extrude it
result = cq.Workplane("XY").circle(rod_diameter / 2.0).extrude(rod_length)