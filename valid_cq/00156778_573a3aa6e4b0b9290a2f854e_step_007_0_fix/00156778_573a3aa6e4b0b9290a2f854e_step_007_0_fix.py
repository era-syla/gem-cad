import cadquery as cq

# Basic dimensions
width = 60
height = 20
thickness = 10
leg_height = 15
leg_width = 10
hole_diameter = 5

# Base block
result = cq.Workplane("XY").rect(width, thickness).extrude(height)

# Create legs
leg = (cq.Workplane("XY")
       .rect(leg_width, thickness)
       .extrude(leg_height)
       .faces(">Z")
       .workplane()
       .circle(hole_diameter/2)
       .cutThruAll())
       
# Position legs
result = (result
          .union(leg.translate((-width/2 + leg_width/2, 0, 0)))
          .union(leg.translate((width/2 - leg_width/2, 0, 0))))

# Rounding corners of the base
result = result.edges("|Z").fillet(3)

# Create holes in the legs
result = (result.faces(">Z")
          .workplane(offset=-leg_height)
          .circle(hole_diameter/2)
          .cutThruAll())