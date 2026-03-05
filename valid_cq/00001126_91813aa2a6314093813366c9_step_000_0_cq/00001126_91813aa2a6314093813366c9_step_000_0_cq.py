import cadquery as cq

# Parametric dimensions
box_length = 60.0
box_width = 30.0
box_height = 30.0
fillet_radius = 2.0

# Bottom large polygon (dodecagon - 12 sides)
bottom_poly_radius = 12.0
bottom_poly_height = 50.0
bottom_poly_sides = 12

# Side small polygon (octagon - 8 sides)
side_poly_radius = 5.0
side_poly_length = 40.0
side_poly_sides = 8

# Create the main rectangular body
# Centered on XY plane, extruded in Z
main_body = cq.Workplane("XY").box(box_length, box_width, box_height)

# Create the bottom vertical extension (large polygon)
# We position it on the bottom face of the main body
bottom_extension = (
    main_body.faces("<Z")
    .workplane()
    .polygon(nSides=bottom_poly_sides, diameter=bottom_poly_radius * 2)
    .extrude(bottom_poly_height)
)

# Create the side horizontal extension (small polygon)
# We position it on the front face of the main body (assuming Y is width)
# Let's adjust based on visual orientation. The image shows the side arm coming out of the 'long' side face.
# If box is created with length (X), width (Y), height (Z), let's assume the arm comes out of -Y or +Y face.
# Looking at the image, if the large cylinder is down (-Z), the main block is top. 
# The arm comes out perpendicular to the cylinder axis.

# Let's restart the construction sequence to keep it clean and joined properly.

# 1. Main Block
main_block = cq.Workplane("XY").box(box_length, box_width, box_height)

# 2. Add Fillets to the top edges of the main block
# Select edges on the top face (>Z)
main_block = main_block.faces(">Z").edges().fillet(fillet_radius)

# 3. Add the bottom column (dodecagon)
# We want to add material downwards from the bottom face.
# Note: By default, extrude adds normal to the plane. The bottom face normal points down (-Z).
# So a positive extrusion length goes downwards.
result_with_bottom = (
    main_block.faces("<Z")
    .workplane(centerOption="CenterOfMass")
    .polygon(nSides=bottom_poly_sides, diameter=bottom_poly_radius * 2)
    .extrude(bottom_poly_height)
)

# 4. Add the side arm (octagon)
# It appears to be centered on one of the larger vertical faces.
# Let's pick the front face (-Y or +Y depending on coord system). 
# Assuming standard orientation, let's pick -Y face.
# We offset the workplane slightly if needed or just use center.
result = (
    result_with_bottom.faces("<Y")
    .workplane(centerOption="CenterOfMass")
    .polygon(nSides=side_poly_sides, diameter=side_poly_radius * 2)
    .extrude(side_poly_length)
)

# Final result variable required
result = result