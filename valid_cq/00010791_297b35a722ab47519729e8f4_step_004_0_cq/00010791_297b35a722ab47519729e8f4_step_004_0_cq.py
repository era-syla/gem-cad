import cadquery as cq

# -- Parametric Dimensions --
# Main flange (large disk)
flange_diameter = 40.0
flange_thickness = 4.0

# Central boss (smaller cylinder)
boss_diameter = 25.0
boss_height = 10.0  # Height protruding from the flange

# Rectangular Through-hole
hole_width = 15.0
hole_height = 8.0

# -- Model Construction --

# 1. Create the base flange (large cylinder)
# We start drawing on the XY plane
base = cq.Workplane("XY").circle(flange_diameter / 2).extrude(flange_thickness)

# 2. Create the boss (smaller cylinder)
# We select the top face of the base and draw the boss
# Note: boss_height is the protrusion length. Total length is flange_thickness + boss_height if measured from bottom
boss = (
    base.faces(">Z")
    .workplane()
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

# 3. Cut the rectangular hole
# The hole goes through the entire object (both boss and flange)
result = (
    boss.faces(">Z")
    .workplane()
    .rect(hole_width, hole_height)
    .cutThruAll()
)

# Alternatively, if the hole is blind or specific depth, we would use .cutBlind(-depth)
# But looking at the image, it implies a through-hole or a deep pocket. 
# Given it's a CAD part likely for a shaft or connector, a through hole is standard.