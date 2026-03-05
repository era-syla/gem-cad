import cadquery as cq

# Parameters
left_tab_length = 20
arch_length = 30
right_slot_length = 20
total_length = left_tab_length + arch_length + right_slot_length
width = 20
plate_thickness = 5
arch_radius = 10
height = plate_thickness + arch_radius

# Create the main block
result = cq.Workplane("XY").box(total_length, width, height, centered=(True, True, False))

# Subtract the interior clamp cylinder
cyl = (
    cq.Workplane("YZ", origin=(
        -total_length/2 + left_tab_length + arch_length/2,
        0,
        plate_thickness
    ))
    .circle(arch_radius)
    .extrude(arch_length)
)
result = result.cut(cyl)

# Create the right-side slot
slot = (
    cq.Workplane("XY")
    .transformed(offset=(
        total_length/2 - right_slot_length/2,
        0,
        height/2
    ))
    .box(right_slot_length, 6, height, centered=(True, True, True))
)
result = result.cut(slot)

# Drill holes on the top face
left_hole_x = -total_length/2 + 10
left_holes = [(left_hole_x, 5), (left_hole_x, -5)]
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(left_holes)
    .hole(6, plate_thickness + 1)
    .pushPoints([(0, 0)])
    .hole(6)
)

result