import cadquery as cq

# Parametric dimensions
length = 150.0       # Total length of the strip
width = 20.0         # Height/Width of the strip
thickness = 3.0      # Thickness of the strip
hole_diameter = 5.0  # Diameter of the mounting holes
hole_offset = 10.0   # Distance from the end edge to the hole center
notch_width = 5.0    # Width of the central notch
notch_depth = 10.0   # Depth of the notch from the top edge

# 1. Create the base rectangular strip
# The box is centered at the origin (0,0,0)
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Create the holes at both ends
# Calculate x position relative to center
h_x = length / 2.0 - hole_offset

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(-h_x, 0), (h_x, 0)])
    .hole(hole_diameter)
)

# 3. Create the rectangular notch on the top edge
# We move the workplane center to the middle of the top edge (0, width/2)
# We draw a rectangle centered at this point. To cut 'notch_depth' into the part,
# the rectangle must extend 'notch_depth' downwards. By making the total height
# 'notch_depth * 2', the rectangle spans equally inside and outside the part edge.
result = (
    result
    .faces(">Z")
    .workplane()
    .moveTo(0, width / 2.0)
    .rect(notch_width, notch_depth * 2)
    .cutThruAll()
)