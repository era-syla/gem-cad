import cadquery as cq

# Parametric dimensions
main_body_diameter = 65.0
main_body_height = 140.0
main_body_fillet_bottom = 2.0

# Upper section parameters
top_dome_height = 10.0
top_neck_diameter = 25.0
top_neck_height = 15.0
rim_diameter = 32.0
rim_thickness = 3.0
inner_hole_diameter = 5.0

# Straw parameters
straw_diameter = 2.0
straw_length = 50.0
straw_angle = 60.0 # Angle downwards from horizontal

# Create the main cylindrical body
body = cq.Workplane("XY").circle(main_body_diameter / 2.0).extrude(main_body_height)

# Add a slight fillet to the bottom edge for realism
body = body.edges("<Z").fillet(main_body_fillet_bottom)

# Create the dome transition at the top
# We'll create a new workplane on top of the body
top_plane = body.faces(">Z").workplane()

# Create the tapered top section (dome/shoulder)
dome = (
    top_plane
    .circle(main_body_diameter / 2.0)
    .workplane(offset=top_dome_height)
    .circle(top_neck_diameter / 2.0)
    .loft(combine=True)
)

# Create the neck/valve assembly area
neck_plane = dome.faces(">Z").workplane()

# The neck cylinder
neck = neck_plane.circle(top_neck_diameter / 2.0).extrude(top_neck_height)

# The rim at the top of the neck (crimped part)
rim_plane = neck.faces(">Z").workplane(offset=-rim_thickness)
rim = rim_plane.circle(rim_diameter / 2.0).extrude(rim_thickness)

# Add the central depressed valve area and the nozzle hole
# First, create a slight depression
valve_cup = (
    rim.faces(">Z").workplane()
    .circle((rim_diameter / 2.0) - 2.0)
    .cutBlind(-2.0)
)

# Create the central boss for the nozzle
nozzle_boss = (
    valve_cup.faces(">Z[1]").workplane() # Select the bottom of the cut we just made
    .circle(inner_hole_diameter * 1.5)
    .extrude(2.0)
)

# Drill the nozzle hole
final_body = (
    nozzle_boss.faces(">Z").workplane()
    .circle(inner_hole_diameter / 2.0)
    .cutBlind(-5.0)
)

# Add grooves/details to the neck/rim for the "crimped" look
neck_groove = (
    final_body.faces(">Z").workplane(offset=-(rim_thickness + 3.0))
    .circle(top_neck_diameter / 2.0 + 1.0) # Slightly wider than neck
    .circle(top_neck_diameter / 2.0 - 0.1) # Cut into neck
    .extrude(1.0)
)

# Create the spray straw
# Position it on the side of the top cap area
straw_start_height = main_body_height + top_dome_height + (top_neck_height / 2.0)
straw_start_radius = top_neck_diameter / 2.0

# Define the path for the straw (straight line sticking out)
straw = (
    cq.Workplane("XZ")
    .transformed(offset=(0, straw_start_height, 0)) # Move up Z
    .transformed(offset=(straw_start_radius - 1.0, 0, 0)) # Move out to radius
    .transformed(rotate=(0, 0, -15)) # Angle slightly downwards (15 deg)
    .circle(straw_diameter / 2.0)
    .extrude(straw_length)
)

# Combine body and straw
result = neck_groove.union(straw)