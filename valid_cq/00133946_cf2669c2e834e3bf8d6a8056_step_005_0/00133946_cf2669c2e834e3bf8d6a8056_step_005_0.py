import cadquery as cq

# Parameters for the geometry
width = 90.0
height = 60.0
thickness = 10.0
fillet_radius = 20.0
cutout_radius = 25.0
hole_diameter = 6.0
arm_hole_x = 35.0  # Distance from center to arm holes
arm_hole_y = 40.0  # Height of arm holes

# Pin/Plunger dimensions
pin_stickout = 10.0
flange_diam = 14.0
flange_thick = 2.0
handle_diam = 10.0
handle_len = 18.0

# Rear tab dimensions
tab_width = 16.0
tab_height = 18.0
tab_depth = 12.0
tab_hole_diam = 5.0

# 1. Create the Main Bracket Body
# Start with a rectangular block
main_body = (
    cq.Workplane("XY")
    .box(width, height, thickness, centered=(True, False, False))
)

# Fillet the top corners to create the rounded arm shape
main_body = main_body.edges("|Z and >Y").fillet(fillet_radius)

# Cut the central U-shaped slot
# We position a circle at the top edge center and cut through
main_body = (
    main_body.faces(">Z").workplane()
    .center(0, height)
    .circle(cutout_radius)
    .cutThruAll()
)

# Cut the mounting holes in the arms
main_body = (
    main_body.faces(">Z").workplane()
    .pushPoints([(-arm_hole_x, arm_hole_y), (arm_hole_x, arm_hole_y)])
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)

# 2. Create the Pin Assembly on the right arm
# Shaft (extends through thickness and sticks out)
shaft = (
    cq.Workplane("XY")
    .circle(hole_diameter / 2.0)
    .extrude(thickness + pin_stickout)
    .translate((arm_hole_x, arm_hole_y, 0))
)

# Flange (stop disk)
flange = (
    cq.Workplane("XY")
    .circle(flange_diam / 2.0)
    .extrude(flange_thick)
    .translate((arm_hole_x, arm_hole_y, thickness + pin_stickout))
)

# Handle (thick cylinder)
handle = (
    cq.Workplane("XY")
    .circle(handle_diam / 2.0)
    .extrude(handle_len)
    .translate((arm_hole_x, arm_hole_y, thickness + pin_stickout + flange_thick))
)
# Add a small chamfer to the handle end for detail
handle = handle.edges(">Z").chamfer(1.0)

# 3. Create the Rear Mounting Tab
# Located at bottom center, protruding from the back face (Negative Z)
tab = (
    cq.Workplane("XY")
    .box(tab_width, tab_height, tab_depth, centered=(True, True, False))
    .translate((0, 0, -tab_depth)) # Move to back side
)

# Cut hole through the tab (X-axis)
tab = (
    tab.faces(">X").workplane()
    .center(0, tab_height / 2.0) # Adjust center relative to the face
    .circle(tab_hole_diam / 2.0)
    .cutThruAll()
)

# Combine all components into the final result
result = main_body.union(shaft).union(flange).union(handle).union(tab)