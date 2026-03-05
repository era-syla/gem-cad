import cadquery as cq

# Base Dimensions
base_length = 250
base_width = 80
base_height = 30
slot_width = 40
slot_depth = 20

# Create Base
base = cq.Workplane("XY").box(base_length, base_width, base_height, centered=(True, True, False))
slot = cq.Workplane("XY").box(base_length, slot_width, slot_depth, centered=(True, True, False)).translate((0, 0, base_height - slot_depth))
base = base.cut(slot)

# Left Block (Bearing Block)
lb_x_center = -110
lb_length = 30
lb_side1 = cq.Workplane("XY").box(lb_length, 20, 10, centered=(True, True, False)).translate((lb_x_center, -30, base_height))
lb_side2 = cq.Workplane("XY").box(lb_length, 20, 10, centered=(True, True, False)).translate((lb_x_center, 30, base_height))
lb_mid = cq.Workplane("XY").box(lb_length, slot_width, 15, centered=(True, True, False)).translate((lb_x_center, 0, base_height))
lb_top = cq.Workplane("YZ").workplane(offset=lb_x_center - lb_length/2).center(0, 45).circle(20).extrude(lb_length)
left_block = lb_side1.union(lb_side2).union(lb_mid).union(lb_top)

# Movable Jaw
mj_x_center = -10
mj_length = 40
mj_base = cq.Workplane("XY").box(mj_length, slot_width, slot_depth, centered=(True, True, False)).translate((mj_x_center, 0, base_height - slot_depth))
mj_mid = cq.Workplane("XY").box(mj_length, base_width, 15, centered=(True, True, False)).translate((mj_x_center, 0, base_height))
mj_top = cq.Workplane("YZ").workplane(offset=mj_x_center - mj_length/2).center(0, 45).circle(20).extrude(mj_length)
movable_jaw = mj_base.union(mj_mid).union(mj_top)

# Fixed Jaw
fj_x_center = 105
fj_length = 40
fixed_jaw = cq.Workplane("XY").box(fj_length, base_width, 35, centered=(True, True, False)).translate((fj_x_center, 0, base_height))

# Jaw Plates
plate_height = 25
plate_thickness = 5
plate_width = 76
plate_z = 40
plate1 = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height, centered=(True, True, False)).translate((82.5, 0, plate_z))
plate2 = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height, centered=(True, True, False)).translate((12.5, 0, plate_z))

# Screw and Handle components
screw_radius = 8
screw_z_center = 45
screw = cq.Workplane("YZ").workplane(offset=-140).center(0, screw_z_center).circle(screw_radius).extrude(130)

smooth_rod = cq.Workplane("YZ").workplane(offset=-140).center(0, screw_z_center).circle(6).extrude(15)
collar = cq.Workplane("YZ").workplane(offset=-155).center(0, screw_z_center).circle(12).extrude(15)

handle_x_center = -147.5
handle_radius = 4
handle_length = 100
handle_rod = cq.Workplane("XZ").workplane(offset=0).center(handle_x_center, screw_z_center).circle(handle_radius).extrude(handle_length, both=True)

ball_radius = 7
ball1 = cq.Workplane("XZ").workplane(offset=handle_length/2).center(handle_x_center, screw_z_center).sphere(ball_radius)
ball2 = cq.Workplane("XZ").workplane(offset=-handle_length/2).center(handle_x_center, screw_z_center).sphere(ball_radius)

# Combine everything into the final result
result = (
    base
    .union(left_block)
    .union(movable_jaw)
    .union(fixed_jaw)
    .union(plate1)
    .union(plate2)
    .union(screw)
    .union(smooth_rod)
    .union(collar)
    .union(handle_rod)
    .union(ball1)
    .union(ball2)
)