import cadquery as cq

# Parameters defining the elliptical plate geometry
plate_major_dia = 180.0
plate_minor_dia = 120.0
plate_height = 12.0
rim_width = 18.0
depression_depth = 8.0  # Leaves 4mm base thickness

# Calculate radii
major_r = plate_major_dia / 2.0
minor_r = plate_minor_dia / 2.0
inner_major_r = major_r - rim_width
inner_minor_r = minor_r - rim_width

# 1. Create the base solid block (Elliptical Cylinder)
result = cq.Workplane("XY").ellipse(major_r, minor_r).extrude(plate_height)

# 2. Fillet the bottom outer edge
# This creates the rounded transition from the side to the bottom
result = result.edges("<Z").fillet(3.0)

# 3. Create the central depression
# We select the top face and cut an ellipse downwards
result = (
    result.faces(">Z")
    .workplane()
    .ellipse(inner_major_r, inner_minor_r)
    .cutBlind(-depression_depth)
)

# 4. Fillet the inner floor edge
# Smooths the transition between the flat bottom and the inner wall
# We identify the floor face by its height
floor_height = plate_height - depression_depth
result = (
    result.faces(cq.NearestToPointSelector((0, 0, floor_height)))
    .edges()
    .fillet(5.0)
)

# 5. Round the top rim
# Apply fillets to both the inner and outer edges of the rim to give it a beaded profile
# We select all edges at the top Z level
result = result.edges(">Z").fillet(4.0)