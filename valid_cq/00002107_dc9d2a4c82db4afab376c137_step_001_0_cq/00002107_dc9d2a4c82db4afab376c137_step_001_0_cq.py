import cadquery as cq

# -- Parametric Dimensions --
length = 60.0       # Overall length of the box
width = 40.0        # Overall width of the box
height = 20.0       # Overall height of the box
vertical_radius = 5.0 # Radius for the vertical corners
top_radius = 2.0    # Radius for the top edge fillet
hole_diameter = 12.0 # Diameter of the off-center hole
hole_offset_x = 15.0 # Distance of the hole from the center along the X-axis

# -- Modeling --

# 1. Create the base rectangular block
# 2. Fillet the vertical edges to get rounded corners
# 3. Fillet the top edge loop for the smooth top transition
# 4. Cut the off-center hole

result = (
    cq.Workplane("XY")
    .box(length, width, height)
    # Select vertical edges (parallel to Z) for filleting
    .edges("|Z")
    .fillet(vertical_radius)
    # Select the top face edges for filleting
    .faces(">Z")
    .edges()
    .fillet(top_radius)
    # Create the hole
    .faces(">Z")
    .workplane()
    .center(hole_offset_x, 0)
    .hole(hole_diameter)
)