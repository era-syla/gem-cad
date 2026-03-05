import cadquery as cq

# Parameters
thickness = 5
L = 80
hook_hole_r = 3
hook_outer_r = hook_hole_r + thickness
plate_half_width = hook_outer_r
plate_width = plate_half_width * 2
hole_d = hook_hole_r * 2
flange_height = 15
flange_hole_offset = 4

# Horizontal plate
plate = (
    cq.Workplane("XY")
    .polyline([
        (0,  plate_half_width),
        (L,  plate_half_width),
        (L, -plate_half_width),
        (0, -plate_half_width)
    ])
    .close()
    .extrude(thickness)
)

# Hook shape: outer disc minus inner hole and minus left half
hook = (
    cq.Workplane("XY")
    .circle(hook_outer_r)
    .extrude(thickness)
    .cut(cq.Workplane("XY").circle(hook_hole_r).extrude(thickness))
    .cut(
        cq.Workplane("XY")
        .box(hook_outer_r, hook_outer_r * 2, thickness, centered=(True, True, False))
        .translate((-hook_outer_r/2, 0, 0))
    )
)

# Combine plate and hook
part = plate.union(hook)

# Vertical flange at right end
flange = (
    cq.Workplane("YZ", origin=(L, 0, 0))
    .transformed(offset=(0, 0, -flange_height/2))
    .rect(plate_width, flange_height)
    .extrude(thickness)
)
part = part.union(flange)

# Cut holes in top of horizontal plate
part = (
    part
    .faces(">Z")
    .workplane()
    .pushPoints([(0, 0), (hook_outer_r + hook_hole_r + 2, 0)])
    .hole(hole_d)
)

# Cut holes in right flange face
part = (
    part
    .faces(">X")
    .workplane()
    .pushPoints([(-flange_hole_offset, 0), (flange_hole_offset, 0)])
    .hole(hole_d)
)

result = part
