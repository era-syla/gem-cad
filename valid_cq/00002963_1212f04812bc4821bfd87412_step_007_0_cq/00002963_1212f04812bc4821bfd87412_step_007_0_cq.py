import cadquery as cq

# -- Parametric Dimensions --
# Base plate dimensions
plate_length = 60.0
plate_width = 30.0
plate_thickness = 2.0

# Stud dimensions
stud_diameter = 10.0
stud_height = 5.0
stud_spacing = 30.0  # Center-to-center distance between studs

# -- Modeling --

# 1. Create the base plate
# We center it on XY plane for easier placement of features later
base = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Create the studs
# We select the top face of the base plate to sketch on
# We create two points for the studs, separated by 'stud_spacing'
# Since the box is centered at (0,0), the points are at (-spacing/2, 0) and (spacing/2, 0)
result = (
    base.faces(">Z")
    .workplane()
    .pushPoints([(-stud_spacing / 2, 0), (stud_spacing / 2, 0)])
    .circle(stud_diameter / 2)
    .extrude(stud_height)
)