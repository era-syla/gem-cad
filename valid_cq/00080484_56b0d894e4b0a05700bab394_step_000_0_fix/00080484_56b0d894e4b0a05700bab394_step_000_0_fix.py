import cadquery as cq

# Parameters
plate_length = 80
plate_width = 60
plate_thickness = 10
tab_radius = 6
hole_diameter = 4
outer_pocket_size = (80, 50)
inner_pocket_size = (50, 30)
outer_pocket_depth = 2
inner_pocket_depth = 2
boss_size = (30, 16)
boss_height = 2
slot_size = (8, 4)
slot_offset_x = 7

result = (
    cq.Workplane("XY")
    # Base plate
    .box(plate_length, plate_width, plate_thickness)
    # Left mounting tab
    .union(
        cq.Workplane("XY")
        .transformed(offset=(-plate_length/2, 0, plate_thickness/2))
        .circle(tab_radius)
        .extrude(-plate_thickness)
    )
    # Right mounting tab
    .union(
        cq.Workplane("XY")
        .transformed(offset=(plate_length/2, 0, plate_thickness/2))
        .circle(tab_radius)
        .extrude(-plate_thickness)
    )
    # Mounting holes (through)
    .faces(">Z").workplane()
    .pushPoints([(-30, 20), (30, 20), (-30, -20), (30, -20), (-plate_length/2, 0), (plate_length/2, 0)])
    .hole(hole_diameter)
    # Outer pocket
    .faces(">Z").workplane()
    .rect(*outer_pocket_size)
    .cutBlind(-outer_pocket_depth)
    # Inner pocket
    .workplane(offset=-outer_pocket_depth)
    .rect(*inner_pocket_size)
    .cutBlind(-inner_pocket_depth)
    # Central boss inside pocket
    .workplane(offset=-(outer_pocket_depth + inner_pocket_depth))
    .rect(*boss_size)
    .extrude(boss_height)
    # Rectangular slots in boss
    .faces(">Z").workplane()
    .pushPoints([(-slot_offset_x, 0), (slot_offset_x, 0)])
    .rect(*slot_size)
    .cutBlind(-boss_height)
)

result  # Final geometry stored in 'result'