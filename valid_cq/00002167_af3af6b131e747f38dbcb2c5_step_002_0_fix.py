import cadquery as cq

# Main base plate (flat, thin)
base_length = 120
base_width = 90
base_height = 4

# Main box on top of base
box_length = 100
box_width = 75
box_height = 25

# Cylinder parameters
cyl_outer_r = 8
cyl_inner_r = 6
cyl_height = 40

# Small feet/legs on the right side
leg_width = 4
leg_depth = 4
leg_height = 10

# Build base plate
base = cq.Workplane("XY").box(base_length, base_width, base_height, centered=(True, True, False))

# Build main box on top of base plate
main_box = (cq.Workplane("XY")
    .workplane(offset=base_height)
    .center(5, 0)  # slight offset to center on base
    .box(box_length, box_width, box_height, centered=(True, True, False))
)

# Combine base and main box
result = base.union(main_box)

# Add cylinder on the left side of the base
cyl_x = -(base_length / 2) + cyl_outer_r + 5
cyl_y = 0
cyl_z = 0

cylinder_outer = (cq.Workplane("XY")
    .workplane(offset=0)
    .center(cyl_x, cyl_y)
    .circle(cyl_outer_r)
    .extrude(cyl_height)
)

# Hollow out the cylinder
cylinder_inner = (cq.Workplane("XY")
    .workplane(offset=2)
    .center(cyl_x, cyl_y)
    .circle(cyl_inner_r)
    .extrude(cyl_height)
)

hollow_cylinder = cylinder_outer.cut(cylinder_inner)

result = result.union(hollow_cylinder)

# Add small legs/feet on the right side bottom
# Two small rectangular legs on right end
leg1_x = base_length / 2 - leg_width / 2 - 2
leg1_y = base_width / 4
leg1_z = -leg_height

leg2_x = base_length / 2 - leg_width / 2 - 2
leg2_y = -base_width / 4

leg1 = (cq.Workplane("XY")
    .workplane(offset=leg1_z)
    .center(leg1_x, leg1_y)
    .box(leg_width, leg_depth, leg_height, centered=(True, True, False))
)

leg2 = (cq.Workplane("XY")
    .workplane(offset=leg2_y)
    .center(leg2_x, leg2_y)
    .box(leg_width, leg_depth, leg_height, centered=(True, True, False))
)

# Actually build legs properly
leg1 = (cq.Workplane("XY")
    .center(leg1_x, leg1_y)
    .box(leg_width, leg_depth, leg_height, centered=(True, True, False))
)

leg2 = (cq.Workplane("XY")
    .center(leg2_x, leg2_y)
    .box(leg_width, leg_depth, leg_height, centered=(True, True, False))
)

# Position legs below base (negative z)
leg1 = (cq.Workplane("XY")
    .workplane(offset=-leg_height)
    .center(leg1_x, leg1_y)
    .rect(leg_width, leg_depth)
    .extrude(leg_height)
)

leg2 = (cq.Workplane("XY")
    .workplane(offset=-leg_height)
    .center(leg2_x, leg2_y)
    .rect(leg_width, leg_depth)
    .extrude(leg_height)
)

result = result.union(leg1).union(leg2)