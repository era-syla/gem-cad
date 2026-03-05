import cadquery as cq

# Parameter definitions
length = 110.0        # Length from hole center to tip
width = 28.0          # Maximum width of the fin
thickness = 6.0       # Thickness of the extruded part
hole_diameter = 10.0  # Diameter of the pivot hole
slot_opening = 7.5    # Width of the rear slot opening
back_overhang = 7.0   # Distance from hole center to the back edge

# Geometric points
# We center the pivot hole at (0,0)
p_tip = (length, 0)
p_back_top = (-back_overhang, width / 2.0)
p_back_bot = (-back_overhang, -width / 2.0)

# Control points for the arc to define the airfoil profile
# These points ensure the curve remains convex and tapered
arc_mid_x = length * 0.35
arc_mid_y = (width / 2.0) * 0.9
p_mid_top = (arc_mid_x, arc_mid_y)
p_mid_bot = (arc_mid_x, -arc_mid_y)

# 1. Generate the main body
# Outline the shape on the XY plane and extrude
main_body = (
    cq.Workplane("XY")
    .moveTo(*p_back_top)
    .threePointArc(p_mid_top, p_tip)      # Upper curved profile
    .threePointArc(p_mid_bot, p_back_bot) # Lower curved profile
    .close()                              # Closes the back edge vertically
    .extrude(thickness)
)

# 2. Create the Snap-Fit Cutout
# Cut the circular hole and the slot leading to the back edge
result = (
    main_body
    .faces(">Z")
    .workplane()
    # Step A: Cut the main pivot hole at the origin
    .moveTo(0, 0)
    .circle(hole_diameter / 2.0)
    .cutThruAll()
    # Step B: Cut the slot opening the hole to the rear
    # Position a rectangle to overlap the back edge and the hole
    .moveTo(-back_overhang, 0)
    .rect(back_overhang * 4.0, slot_opening) # Width ensures it cuts through the back face
    .cutThruAll()
)