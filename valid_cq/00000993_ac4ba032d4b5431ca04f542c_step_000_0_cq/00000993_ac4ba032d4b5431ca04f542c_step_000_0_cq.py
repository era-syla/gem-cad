import cadquery as cq

# Parametric dimensions
length = 200.0   # Total length of the bar
width = 15.0     # Width of the bar
thickness = 2.0  # Thickness of the bar
hole_diameter = 6.0 # Diameter of the holes

# Hole positions along the length (relative to the center)
# The image shows two holes near one end and one hole near the other end.
# Let's assume a coordinate system centered on the bar.
# Total length is 200.
# Left end is at x = -100, Right end is at x = 100.
# Let's place:
# - One hole near the left end: x = -85
# - One hole near the right end: x = 85
# - A third hole near the right end, inboard: x = 50 
# (The image shows an asymmetry: one hole at one end, two at the other)
# Adjusting based on visual estimation:
# Let's say the single hole is on the left, and the pair is on the right.
single_hole_pos = -length/2 + 15.0  # Near the left edge
double_hole_1_pos = length/2 - 15.0 # Near the right edge
double_hole_2_pos = length/2 - 55.0 # Further in from the right edge

# Create the base rectangular bar
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .faces(">Z")
    .workplane()
)

# Create the list of hole centers
hole_centers = [
    (single_hole_pos, 0),
    (double_hole_1_pos, 0),
    (double_hole_2_pos, 0)
]

# Cut the holes
result = (
    result
    .pushPoints(hole_centers)
    .hole(hole_diameter)
)