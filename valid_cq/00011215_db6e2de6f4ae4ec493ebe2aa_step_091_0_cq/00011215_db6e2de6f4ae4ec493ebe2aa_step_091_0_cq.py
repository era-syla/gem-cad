import cadquery as cq

# Parametric Dimensions
rod_diameter = 1.0       # Diameter of the main rod
rod_length = 200.0       # Total length of the main rod section
top_extension = 15.0     # Length of the section above the stopper
stopper_diameter = 4.0   # Diameter of the stopper/knot feature
stopper_height = 5.0     # Height of the stopper/knot feature
tip_diameter = 2.0       # Diameter of the top tip
tip_height = 3.0         # Height of the top tip

# 1. Create the Main Rod
# We start from the origin and go up
main_rod = cq.Workplane("XY").circle(rod_diameter / 2).extrude(rod_length)

# 2. Create the Stopper/Junction
# Located at the top of the main rod
# We'll model this as a slightly complex shape to mimic the "knot" or mechanical fastener look
# It's roughly cylindrical but with some irregularity, simplified here as a chamfered cylinder
stopper = (
    cq.Workplane("XY")
    .workplane(offset=rod_length)
    .circle(stopper_diameter / 2)
    .extrude(stopper_height)
    .faces(">Z").chamfer(0.5)
    .faces("<Z").chamfer(0.5)
)

# 3. Create the Top Extension Rod
# Extends from the top of the stopper
extension_rod = (
    cq.Workplane("XY")
    .workplane(offset=rod_length + stopper_height)
    .circle(rod_diameter / 2)
    .extrude(top_extension)
)

# 4. Create the Tip Connector
# Located at the very top
tip = (
    cq.Workplane("XY")
    .workplane(offset=rod_length + stopper_height + top_extension)
    .circle(tip_diameter / 2)
    .extrude(tip_height)
    .faces(">Z").fillet(0.2) # Round off the top slightly
)

# Combine all parts into a single solid
result = main_rod.union(stopper).union(extension_rod).union(tip)