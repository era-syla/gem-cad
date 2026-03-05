import cadquery as cq

# Parameters based on visual estimation of the provided image
# The object resembles a shotgun shell hull or a similar cylindrical casing.
height = 80.0
outer_diameter = 26.0
radius = outer_diameter / 2.0
wall_thickness = 2.0
base_height = 22.0  # Height of the bottom section (metal head area)
groove_width = 0.5  # Width of the transition line
groove_depth = 0.3  # Depth of the transition line
bottom_fillet_radius = 1.0

# 1. Create the main solid cylinder
# We start with a solid cylinder extruded from the XY plane.
base_geo = cq.Workplane("XY").circle(radius).extrude(height)

# 2. Apply fillet to the bottom edge
# This is done before shelling to create a rounded internal corner as well,
# maintaining consistent wall thickness, or simply to round the exterior.
base_geo = base_geo.faces("<Z").edges().fillet(bottom_fillet_radius)

# 3. Shell the object to make it hollow
# Selecting the top face (">Z") and shelling with negative thickness creates 
# an open container (cup/tube shape) with inward thickness.
hollow_geo = base_geo.faces(">Z").shell(-wall_thickness)

# 4. Create the detail groove
# This groove separates the base section from the upper body.
# We create a ring-shaped solid (tube) to act as a cutter.
groove_cutter = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .circle(radius + 1.0)           # Outer circle (outside the part)
    .circle(radius - groove_depth)  # Inner circle (defines cut depth)
    .extrude(groove_width)
)

# 5. Apply the cut to the main geometry
result = hollow_geo.cut(groove_cutter)