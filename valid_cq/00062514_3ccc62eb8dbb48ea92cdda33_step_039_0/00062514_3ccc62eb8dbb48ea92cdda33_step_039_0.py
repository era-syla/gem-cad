import cadquery as cq

# Parametric dimensions of the beam
length = 100.0       # Total vertical length
width = 10.0         # Overall width of the cross-section
thickness = 3.33     # Thickness of the cross arms (approx 1/3 of width)

# Method: Create two overlapping rectangular prisms and union them to form the cross shape

# 1. Create the first rectangular prism aligned with the X-axis
# Centered on XY plane, extruded along Z
beam_x = cq.Workplane("XY").rect(width, thickness).extrude(length)

# 2. Create the second rectangular prism aligned with the Y-axis
beam_y = cq.Workplane("XY").rect(thickness, width).extrude(length)

# 3. Create the final geometry by unioning the two prisms
result = beam_x.union(beam_y)