import cadquery as cq

# Parameters
length = 80.0
width = 30.0
thickness = 5.0
fillet_radius = 3.0

boss_base_dia = 24.0
boss_top_dia = 12.0
cone_height = 12.0
flange_height = 3.0

hole_dia = 6.0
hole_offset = length/2 - 10.0

# Build the base plate
result = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(thickness)
    .edges("|Z")
    .fillet(fillet_radius)
    # Build the conical boss
    .faces(">Z")
    .workplane()
    .circle(boss_base_dia/2)
    .workplane(offset=cone_height)
    .circle(boss_top_dia/2)
    .loft()
    # Build the top flange
    .faces(">Z")
    .workplane()
    .circle(boss_top_dia/2)
    .extrude(flange_height)
    # Drill the central hole through boss and plate
    .faces(">Z")
    .workplane()
    .circle(hole_dia/2)
    .cutThruAll()
    # Drill the two mounting holes in the plate
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_offset, 0), (hole_offset, 0)])
    .circle(hole_dia/2)
    .cutThruAll()
)