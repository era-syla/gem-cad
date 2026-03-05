import cadquery as cq

# Parametric dimensions
outer_diameter = 50.0  # Overall diameter of the cylinder
length = 80.0          # Total length of the cylinder
wall_thickness = 2.0   # Thickness of the outer wall
inset_depth = 5.0      # How far the inner face is recessed

# Calculate derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the main cylinder
main_body = cq.Workplane("XY").circle(outer_radius).extrude(length)

# Create the recess (pocket) at the front face
# We select the top face (Z-positive), sketch a circle for the inner diameter, 
# and cut down by the inset_depth.
result = (
    main_body
    .faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutBlind(-inset_depth)
)

# Optional: If the cylinder needs to be hollow all the way through like a pipe:
# result = main_body.faces(">Z").workplane().circle(inner_radius).cutThruAll()
# But based on the image, it looks like a solid plug or a capped tube, 
# where we can see a distinct recessed face rather than a through-hole.
# The code above produces the recessed face look.