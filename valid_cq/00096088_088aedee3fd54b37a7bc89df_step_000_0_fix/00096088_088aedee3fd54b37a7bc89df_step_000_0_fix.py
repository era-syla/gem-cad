import cadquery as cq

# Base plate
result = cq.Workplane("XZ").box(80, 5, 200)

# Rectangular pocket on front face
result = result.faces(">Y").workplane().rect(30, 15).cutBlind(-4)

# Horizontal bar protrusion
result = result.faces(">Y").workplane().rect(60, 8).extrude(6)

# Vertical bar protrusion
result = result.faces(">Y").workplane().rect(8, 60).extrude(6)

# Small cylindrical pin below center
result = result.faces(">Y").workplane().center(0, -80).circle(3).extrude(12)