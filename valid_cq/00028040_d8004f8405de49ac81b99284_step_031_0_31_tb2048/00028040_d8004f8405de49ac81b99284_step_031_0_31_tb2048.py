import cadquery as cq

# Parametric dimensions
length = 100.0
step_x = 60.0

height_left = 30.0
height_right = 40.0

y_front_pad = 5.0
y_main = 15.0
y_slot = 5.0
y_back = 5.0

z_slot = 10.0
z_back = 20.0

hole_rad = 3.0

# 1. Left main block
part = cq.Workplane("XY").box(
    step_x, y_main, height_left
).translate((
    step_x / 2.0, 
    y_front_pad + y_main / 2.0, 
    height_left / 2.0
))

# 2. Right main block
part = part.union(
    cq.Workplane("XY").box(
        length - step_x, y_main, height_right
    ).translate((
        step_x + (length - step_x) / 2.0, 
        y_front_pad + y_main / 2.0, 
        height_right / 2.0
    ))
)

# 3. Back slot base
part = part.union(
    cq.Workplane("XY").box(
        length, y_slot, z_slot
    ).translate((
        length / 2.0, 
        y_front_pad + y_main + y_slot / 2.0, 
        z_slot / 2.0
    ))
)

# 4. Back wall
part = part.union(
    cq.Workplane("XY").box(
        length, y_back, z_back
    ).translate((
        length / 2.0, 
        y_front_pad + y_main + y_slot + y_back / 2.0, 
        z_back / 2.0
    ))
)

# 5. Front L-shape vertical arm
v_arm_w = 10.0
v_arm_h = 20.0
v_arm_z = 5.0
part = part.union(
    cq.Workplane("XY").box(
        v_arm_w, y_front_pad, v_arm_h
    ).translate((
        step_x - v_arm_w / 2.0, 
        y_front_pad / 2.0, 
        v_arm_z + v_arm_h / 2.0
    ))
)

# 6. Front L-shape horizontal arm
h_arm_l = 15.0
h_arm_h = 5.0
h_arm_z = 20.0
part = part.union(
    cq.Workplane("XY").box(
        h_arm_l, y_front_pad, h_arm_h
    ).translate((
        step_x - v_arm_w - h_arm_l / 2.0, 
        y_front_pad / 2.0, 
        h_arm_z + h_arm_h / 2.0
    ))
)

# 7. Drill holes
hole_pts = [
    (20.0, 15.0),  # Left top hole
    (20.0, 5.0),   # Left bottom hole
    (85.0, 25.0)   # Right hole
]

# Create a cutting tool for the holes on the XZ plane (extruding along Y)
cutter = cq.Workplane("XZ", origin=(0, 0, 0)).pushPoints(hole_pts).cylinder(100.0, hole_rad)

# Final part
result = part.cut(cutter)