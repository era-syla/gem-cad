import cadquery as cq

# Parametric Dimensions
cylinder_diameter = 40.0
cylinder_height = 25.0
hex_width_across_flats = 12.0  # Size of the hex socket
hex_depth = 8.0               # Depth of the hex socket
through_hole_diameter = 6.0   # Diameter of the hole at the bottom of the hex

# Create the base cylinder
result = cq.Workplane("XY").circle(cylinder_diameter / 2.0).extrude(cylinder_height)

# Create the hexagonal socket on the top face
# polygon(6, ...) creates a hexagon. The diameter argument for polygon is usually circumscribed circle.
# To get width across flats (W), the radius (r) of the circumcircle is W / sqrt(3).
# However, CadQuery's polygon diameter often refers to the circle passing through vertices.
# Let's calculate the circumradius based on flat-to-flat distance.
# R = (W / 2) / cos(30 deg) = W / sqrt(3)
# Diameter = 2 * R
circum_diameter = 2 * (hex_width_across_flats / 2.0) / 0.8660254 # approx sqrt(3)/2

result = (result.faces(">Z")
          .workplane()
          .polygon(nSides=6, diameter=circum_diameter)
          .cutBlind(-hex_depth))

# Create the through-hole at the bottom of the hex socket
# Note: The image shows a hole continuing down. It might be blind or through. 
# Assuming a standard bolt-like or spacer geometry, a through hole is common, 
# or at least a pilot hole. I'll make it a through hole for utility.
result = (result.faces("<Z")
          .workplane()
          .circle(through_hole_diameter / 2.0)
          .cutThruAll())

# If the hole was meant to start from the bottom of the hex, we could do this instead:
# result = result.faces(">Z").workplane().circle(through_hole_diameter / 2.0).cutThruAll() 
# But selecting <Z and cutting up is robust.