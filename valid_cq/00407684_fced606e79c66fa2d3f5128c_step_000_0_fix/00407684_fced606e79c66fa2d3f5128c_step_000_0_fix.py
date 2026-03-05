import cadquery as cq

# Parameters
R_main = 20
arm_len = 30
arm_half_width = 6
base_thickness = 4
pad_rad = 6
pad_height = 4
boss_rad = 3
boss_height = 6
hole_main = 4
hole_offset = 3
hole_pad = 4
hole_boss = 3

# Build the base plate (central disc + two rectangular arms)
base = (
    cq.Workplane("XY")
    .circle(R_main).extrude(base_thickness)
    .union(
        cq.Workplane("XY")
        .rect(arm_len, arm_half_width * 2)
        .extrude(base_thickness)
        .translate(( R_main + arm_len/2, 0, 0))
    )
    .union(
        cq.Workplane("XY")
        .rect(arm_len, arm_half_width * 2)
        .extrude(base_thickness)
        .translate((-R_main - arm_len/2, 0, 0))
    )
)
# Drill holes in the base
base = (
    base.faces(">Z").workplane()
    .pushPoints([(0, 0)]).hole(hole_main)
    .pushPoints([(-10, 0)]).hole(hole_offset)
)

# Left pad with through hole
pad_left = (
    cq.Workplane("XY")
    .circle(pad_rad).extrude(pad_height)
    .translate((-R_main - arm_len, 0, base_thickness))
    .faces(">Z").workplane()
    .hole(hole_pad)
)

# Right pad with through hole
pad_right = (
    cq.Workplane("XY")
    .circle(pad_rad).extrude(pad_height)
    .translate(( R_main + arm_len, 0, base_thickness))
    .faces(">Z").workplane()
    .hole(hole_pad)
)

# Boss on right pad with hole
boss = (
    cq.Workplane("XY")
    .circle(boss_rad).extrude(boss_height)
    .translate(( R_main + arm_len, 0, base_thickness + pad_height))
    .faces(">Z").workplane()
    .hole(hole_boss)
)

# Combine everything
result = base.union(pad_left).union(pad_right).union(boss)