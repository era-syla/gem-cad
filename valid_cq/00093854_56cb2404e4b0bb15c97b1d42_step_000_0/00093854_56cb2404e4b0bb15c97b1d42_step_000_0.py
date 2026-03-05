import cadquery as cq

# Parametric dimensions for the model
length = 100.0
width = 40.0
height = 20.0

# Top face hole dimensions
top_center_hole_dia = 24.0
top_side_hole_dia = 12.0
top_side_hole_spacing = 70.0  # Distance between the two outer holes

# Side face hole dimensions
side_hole_dia = 8.0
side_hole_spacing = 40.0  # Distance between the two side holes

# 1. Create the base rectangular block
# We center it at the origin to make symmetry operations easier
result = cq.Workplane("XY").box(length, width, height)

# 2. Add features to the Top Face
# Select the top face (+Z) and create a workplane
result = (
    result.faces(">Z")
    .workplane()
    # Cut the large center hole
    .hole(top_center_hole_dia)
    # Cut the two smaller outer holes
    .pushPoints([(-top_side_hole_spacing / 2, 0), (top_side_hole_spacing / 2, 0)])
    .hole(top_side_hole_dia)
)

# 3. Add features to the Side Face
# Select the front face (+Y) and create a workplane
# Note: Since we use hole(), it will drill through the entire width
result = (
    result.faces(">Y")
    .workplane()
    # Define positions for the side holes (staggered relative to top holes)
    .pushPoints([(-side_hole_spacing / 2, 0), (side_hole_spacing / 2, 0)])
    .hole(side_hole_dia)
)