import cadquery as cq

# Parametric dimensions
base_diameter = 40.0
base_height = 10.0
post_diameter = 18.0
post_height = 30.0
hole_diameter = 10.0
slit_width = 3.0
chamfer_size = 1.5

# Create the base cylinder
base = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_height)

# Create the main post cylinder on top of the base
post = (
    base.faces(">Z")
    .workplane()
    .circle(post_diameter / 2)
    .extrude(post_height)
)

# Combine base and post (often automatic in recent CQ versions if using the stack, but good to be explicit for 'result')
main_body = post

# Create the through hole
with_hole = main_body.faces(">Z").workplane().hole(hole_diameter)

# Create the slit
# We select the top face, draw a rectangle centered on the origin, and cut it down
# The depth of the slit appears to go most of the way down the post, but not into the base.
slit_depth = post_height * 0.85 

with_slit = (
    with_hole.faces(">Z")
    .workplane()
    .rect(base_diameter, slit_width) # Make the rectangle wide enough to cut through the whole diameter
    .cutBlind(-slit_depth)
)

# Add chamfer to the top outer edge of the post
# We need to select the edge carefully. It's the outer circle at the highest Z.
final_geometry = (
    with_slit.faces(">Z")
    .edges(cq.selectors.RadiusNthSelector(1)) # Selects the outer radius edge (hole is inner)
    .chamfer(chamfer_size)
)

result = final_geometry