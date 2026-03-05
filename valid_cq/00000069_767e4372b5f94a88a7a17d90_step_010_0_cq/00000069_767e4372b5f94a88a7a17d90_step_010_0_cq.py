import cadquery as cq

# Parameters
plate_length = 60.0
plate_height = 25.0
plate_thickness = 3.0

central_cutout_width = 15.0
central_cutout_height = 15.0

corner_fillet_radius = 4.0

mounting_hole_diameter = 3.5
mounting_hole_spacing = 45.0  # Distance between hole centers

# Recess parameters (the thinner section around the cutout)
recess_width = 25.0   # Wider than cutout
recess_height = 25.0  # Same as plate height (cuts through top/bottom)
recess_depth = 1.5    # Depth of the recess cut

# Create the base plate
base = (
    cq.Workplane("XY")
    .box(plate_length, plate_height, plate_thickness)
    .edges("|Z")
    .fillet(corner_fillet_radius)
)

# Create the central square cutout
result = (
    base
    .faces(">Z")
    .workplane()
    .rect(central_cutout_width, central_cutout_height)
    .cutThruAll()
)

# Create the recess (the stepped area around the central hole)
# The image shows a recessed area on one face, wider than the hole,
# extending to the top and bottom edges.
result = (
    result
    .faces(">Z")
    .workplane()
    .rect(recess_width, plate_height) # Height matches plate to cut through edges
    .cutBlind(-recess_depth)
)

# Create the mounting holes
# Positioned symmetrically relative to the center
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(-mounting_hole_spacing/2, 0), (mounting_hole_spacing/2, 0)])
    .hole(mounting_hole_diameter)
)

# Final result is stored in 'result' variable as requested