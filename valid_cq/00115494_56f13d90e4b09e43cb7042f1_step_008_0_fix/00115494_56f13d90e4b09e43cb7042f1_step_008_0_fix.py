import cadquery as cq

# Parameters
base_height = 30
base_diameter = 20
ball_radius = 10
collar_thickness = 4
collar_outer = ball_radius * 2.2
screw_height = 3
screw_diameter = ball_radius * 1.2
slot_length = screw_diameter * 0.8
slot_width = screw_height * 1.5
rod_diameter = 4
rod_length = 120
rod_angle = -30  # degrees

# Base cylinder
base = cq.Workplane("XY").cylinder(base_height, base_diameter / 2)

# Ball joint
ball = cq.Workplane("XY").workplane(offset=base_height + ball_radius).sphere(ball_radius)

# Collar around ball
collar = cq.Workplane("XY").workplane(offset=base_height + ball_radius).cylinder(collar_thickness, collar_outer / 2)

# Screw head on top
screw = cq.Workplane("XY").workplane(offset=base_height + 2*ball_radius + collar_thickness).cylinder(screw_height, screw_diameter / 2)
# Slot in screw head
slot = (cq.Workplane("XY")
        .workplane(offset=base_height + 2*ball_radius + collar_thickness - 1)
        .rect(slot_length, slot_width)
        .extrude(screw_height + 2))
screw = screw.cut(slot)

# Rod at angle
rod = (cq.Workplane("XY")
       .workplane(offset=base_height + 2*ball_radius + collar_thickness)
       .transformed(rotate=(0, rod_angle, 0))
       .cylinder(rod_length, rod_diameter / 2))

result = base.union(ball).union(collar).union(screw).union(rod)