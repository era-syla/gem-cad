import cadquery as cq

# Parametric Dimensions
length = 80.0       # Total length of the bracket
width = 15.0        # Width of the bracket
thickness = 3.0     # Base plate thickness
fillet_radius = width / 2.0 # Round ends

# Hole Parameters
hole_offset = 6.0   # Distance from the rounded edge center to the hole center
hole_diameter = 4.0 # Diameter of the mounting holes
countersink_dia = 7.0 # Diameter of the countersink
countersink_angle = 90.0 # Standard countersink angle

# Post Parameters
post_offset = 18.0  # Distance from center to post
post_diameter = 3.5 # Diameter of the vertical posts
post_height = 10.0  # Height of the posts from the top surface

# Create the base shape (rounded rectangle)
# We extrude a rectangle and fillet the vertical edges to create the "stadium" shape
base = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(thickness)
    .edges("|Z")
    .fillet(fillet_radius - 0.01) # Slightly less than half width to ensure stability, or use exact math
)

# Add countersunk holes at the ends
# We need to position them relative to the ends.
# The total length is 'length', so ends are at +/- length/2
hole_x_pos = (length / 2.0) - hole_offset

base_with_holes = (
    base.faces(">Z")
    .workplane()
    .pushPoints([(hole_x_pos, 0), (-hole_x_pos, 0)])
    .cskHole(hole_diameter, countersink_dia, countersink_angle)
)

# Add the vertical posts
# These are positioned inwards from the holes
post_x_pos = (length / 2.0) - post_offset

result = (
    base_with_holes.faces(">Z")
    .workplane()
    .pushPoints([(post_x_pos, 0), (-post_x_pos, 0)])
    .circle(post_diameter / 2.0)
    .extrude(post_height)
)

# Optional: Add small fillets to the base of the posts for strength/visuals (inferred from smooth transitions often found in molding)
# result = result.faces(">Z").edges(cq.selectors.RadiusNthSelector(0)).fillet(0.5) 
# (Skipping strictly as it's hard to see in the low-res image, sticking to primary geometry)