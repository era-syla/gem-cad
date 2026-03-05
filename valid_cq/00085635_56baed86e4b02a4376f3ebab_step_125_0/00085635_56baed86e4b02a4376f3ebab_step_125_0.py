import cadquery as cq

# Part Parameters
plate_length = 100.0
plate_width = 20.0
plate_thickness = 2.0
fillet_radius = 4.0

boss_outer_diameter = 8.0
boss_inner_diameter = 4.5
boss_height = 2.0
hole_spacing = 80.0  # Distance between the centers of the two bosses

# 1. Create the base plate
# Draw a box centered at the origin
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# Fillet the vertical edges to create rounded corners
result = result.edges("|Z").fillet(fillet_radius)

# 2. Add the bosses (standoffs)
# Select the top face of the plate
# Push two points for the locations of the bosses
# Draw the outer circles and extrude them upwards
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing / 2, 0), (hole_spacing / 2, 0)])
    .circle(boss_outer_diameter / 2)
    .extrude(boss_height)
)

# 3. Cut the through-holes
# Select the top face of the newly created bosses
# Push the same two points
# Draw the inner circles and cut through the entire part
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing / 2, 0), (hole_spacing / 2, 0)])
    .circle(boss_inner_diameter / 2)
    .cutThruAll()
)