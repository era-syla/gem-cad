import cadquery as cq

# Parametric dimensions
outer_diameter = 20.0
inner_diameter = 8.0
thickness = 3.0

# Create the washer geometry
# Method 1: Create a circle, extrude it, then cut a hole
# result = (cq.Workplane("XY")
#           .circle(outer_diameter / 2)
#           .extrude(thickness)
#           .faces(">Z")
#           .hole(inner_diameter))

# Method 2: Create two concentric circles and extrude the difference (more robust)
result = (cq.Workplane("XY")
          .circle(outer_diameter / 2)
          .circle(inner_diameter / 2)
          .extrude(thickness))