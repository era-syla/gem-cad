import cadquery as cq

# Dimensions based on visual analysis
length = 80.0
width = 30.0
height = 30.0
arch_radius = 14.0
hole_spacing = 54.0
hole_dia = 6.5
cs_dia = 13.0
cs_angle = 90.0
recess_width = 34.0  # Width of the central recessed section creating the vertical lines
recess_depth = 2.0   # Depth of the step on the side faces

# 1. Base Geometry: Create the main rectangular block
# Centered at (0,0,0) so Z ranges from -15 to +15
result = cq.Workplane("XY").box(length, width, height)

# 2. Side Recesses: Cut rectangular pockets on the front and back faces
# These create the vertical feature lines and the stepped side profile visible in the image.
# We cut on the >Y (Front) and <Y (Back) faces.
result = (
    result.faces(">Y").workplane()
    .center(0, 0)
    .rect(recess_width, height)
    .cutBlind(-recess_depth)
)

result = (
    result.faces("<Y").workplane()
    .center(0, 0)
    .rect(recess_width, height)
    .cutBlind(-recess_depth)
)

# 3. Arch Feature: Cut a semi-cylinder from the bottom face
# We select the bottom face (<Z), rotate the workplane 90 degrees to align with the Y-axis,
# draw the circle, and cut through the entire part.
result = (
    result.faces("<Z").workplane(centerOption="CenterOfMass")
    .transformed(rotate=(90, 0, 0))
    .circle(arch_radius)
    .cutThruAll()
)

# 4. Mounting Holes: Create countersunk holes on the top face
result = (
    result.faces(">Z").workplane()
    .pushPoints([(-hole_spacing/2, 0), (hole_spacing/2, 0)])
    .cskHole(hole_dia, cs_dia, cs_angle)
)