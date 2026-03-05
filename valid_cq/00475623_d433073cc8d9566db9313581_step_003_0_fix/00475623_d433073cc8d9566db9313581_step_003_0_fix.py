import cadquery as cq

# Parameters
plate_len = 80
plate_w = 40
plate_h = 10
arch_radius = 30
arch_thickness = 5
support_th = 8
arm_len = 120
arm_w_root = 20
arm_w_tip = 6
arm_th = 4
hole_d = 4

# Top plate
plate = cq.Workplane("XY").box(plate_len, plate_w, plate_h)

# Half-cylinder arch under plate
arch = (
    cq.Workplane("XZ", origin=(0, -plate_h/2, 0))
    .moveTo(-plate_len/2, arch_radius)
    .threePointArc((0, -arch_radius), (plate_len/2, arch_radius))
    .lineTo(plate_len/2, arch_radius - arch_thickness)
    .threePointArc((0, -arch_radius + arch_thickness), (-plate_len/2, arch_radius - arch_thickness))
    .close()
    .extrude(plate_w)
)

# Triangular supports under plate
support = (
    cq.Workplane("XY", origin=(0,0,-plate_h/2))
    .polyline([(-plate_len/2, -plate_w/2), (0, -plate_w/2 - 15), (plate_len/2, -plate_w/2)])
    .close()
    .extrude(support_th)
)

# Arm extending to the right
arm = (
    cq.Workplane("XY", origin=(plate_len/2, 0, plate_h/2))
    .polyline([
        (0,  arm_w_root/2),
        (arm_len,  arm_w_tip/2),
        (arm_len, -arm_w_tip/2),
        (0, -arm_w_root/2)
    ])
    .close()
    .extrude(arm_th)
)

# Three holes at arm tip
arm = (
    arm.faces(">X")
       .workplane(centerOption="CenterOfBoundBox")
       .pushPoints([
           (arm_len - 5,  0),
           (arm_len - 5,  arm_w_tip/3),
           (arm_len - 5, -arm_w_tip/3),
       ])
       .hole(hole_d)
)

# Combine all parts
result = plate.union(arch).union(support).union(arm)