import cadquery as cq

# Base plate
base = cq.Workplane("XY").box(120, 80, 5)

# Add corner mounting holes/bosses to base
base = base.faces(">Z").workplane().rect(100, 60, forConstruction=True).vertices().circle(4).extrude(3)

# Support columns (left and right)
col_left = cq.Workplane("XY").center(-35, 0).circle(5).extrude(50)
col_right = cq.Workplane("XY").center(35, 0).circle(5).extrude(50)

# Column top caps
cap_left = cq.Workplane("XY").center(-35, 0).workplane(offset=50).circle(7).extrude(4)
cap_right = cq.Workplane("XY").center(35, 0).workplane(offset=50).circle(7).extrude(4)

# Main flywheel ring (large circular ring on right side)
wheel_center_x = 30
wheel_center_y = 0
wheel_outer_r = 38
wheel_inner_r = 33
wheel_z = 2.5  # starts at top of base

flywheel = (cq.Workplane("YZ")
    .center(wheel_center_y, wheel_z + 45)
    .circle(wheel_outer_r)
    .circle(wheel_inner_r)
    .extrude(6))

# Flywheel spoke - horizontal bar through center
spoke_h = (cq.Workplane("XY")
    .workplane(offset=wheel_z + 45)
    .center(wheel_center_x, wheel_center_y)
    .rect(76, 4)
    .extrude(6))

spoke_v = (cq.Workplane("XY")
    .workplane(offset=wheel_z + 45)
    .center(wheel_center_x, wheel_center_y)
    .rect(4, 76)
    .extrude(6))

# Central axle
axle = (cq.Workplane("XY")
    .workplane(offset=5)
    .center(0, 0)
    .circle(4)
    .extrude(55))

# Left paddle/vane (rectangular plate on left)
vane_left = (cq.Workplane("XY")
    .workplane(offset=30)
    .center(-50, 5)
    .rect(20, 25)
    .extrude(3))

# Coil/spring assembly in center (simplified as cylinders)
coil1 = (cq.Workplane("XY")
    .workplane(offset=35)
    .center(-8, 0)
    .circle(6)
    .extrude(20))

coil2 = (cq.Workplane("XY")
    .workplane(offset=35)
    .center(8, 0)
    .circle(6)
    .extrude(20))

# Inner coil details
coil1_inner = (cq.Workplane("XY")
    .workplane(offset=35)
    .center(-8, 0)
    .circle(4)
    .extrude(20))

coil2_inner = (cq.Workplane("XY")
    .workplane(offset=35)
    .center(8, 0)
    .circle(4)
    .extrude(20))

# Small gear/sprocket at bottom center
gear = (cq.Workplane("XY")
    .workplane(offset=8)
    .center(5, 0)
    .circle(10)
    .extrude(6))

# Small box component on right side (motor/actuator)
box_comp = (cq.Workplane("XY")
    .workplane(offset=8)
    .center(50, -15)
    .rect(18, 12)
    .extrude(8))

# Left support arm diagonal
left_arm = (cq.Workplane("XY")
    .workplane(offset=5)
    .center(-40, 0)
    .circle(4)
    .extrude(45))

# Assemble all parts
result = (base
    .union(col_left)
    .union(col_right)
    .union(cap_left)
    .union(cap_right)
    .union(flywheel)
    .union(spoke_h)
    .union(spoke_v)
    .union(axle)
    .union(vane_left)
    .union(coil1)
    .union(coil2)
    .union(gear)
    .union(box_comp)
    .union(left_arm)
)