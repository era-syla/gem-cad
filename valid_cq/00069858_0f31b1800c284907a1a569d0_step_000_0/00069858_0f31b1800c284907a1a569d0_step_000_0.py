import cadquery as cq

# Parametric dimensions
length = 120.0
width = 20.0
height = 20.0

# Top hole parameters
top_hole_diameter = 6.0
top_hole_spacing_inner = 50.0  # Distance between the two inner holes
top_hole_spacing_outer = 90.0  # Distance between the two outer holes

# Side cutout parameters (figure-8 shape)
side_cut_diameter = 10.0
side_cut_center_dist = 7.0     # Distance between the centers of the two overlapping circles

# Create the base rectangular prism
result = cq.Workplane("XY").box(length, width, height)

# Create the holes on the top face
# Calculate x-coordinates for the holes
pts = [
    (-top_hole_spacing_outer / 2, 0),
    (-top_hole_spacing_inner / 2, 0),
    (top_hole_spacing_inner / 2, 0),
    (top_hole_spacing_outer / 2, 0)
]

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(pts)
    .hole(top_hole_diameter)
)

# Create the intersecting hole cutout on the side face
# This creates two overlapping holes to form the specific shape shown
side_pts = [
    (-side_cut_center_dist / 2, 0),
    (side_cut_center_dist / 2, 0)
]

result = (
    result
    .faces(">Y")
    .workplane()
    .pushPoints(side_pts)
    .hole(side_cut_diameter)
)