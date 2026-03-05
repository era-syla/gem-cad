import cadquery as cq

# Parameters
plate_length = 120
plate_width = 60
plate_thickness = 5
hole_diameter = 5
hole_depth = 6
hole_positions = [(-40, -20), (-40, 20), (40, -20), (40, 20)]

disc_radius = 20
disc_thickness = 8
disc_hole_radius_positions = [(12, 0), (0, 12), (-12, 0), (0, -12)]
disc_hole_diameter = 5
disc_hole_depth = disc_thickness

support_length = disc_thickness
support_width = 30
support_height = 10
support_positions = [(-6, 0), (6, 0)]

shaft_radius = 5
shaft_length = 12
shaft_start = -2

nozzle_base_radius = shaft_radius
nozzle_tip_radius = 1
nozzle_length = 20
nozzle_start = shaft_start + shaft_length

# Base plate
plate = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness, centered=(True, True, False))
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter, hole_depth)
)

# Supports
supports = (
    cq.Workplane("XY")
    .pushPoints(support_positions)
    .rect(support_length, support_width)
    .extrude(support_height)
)

# Discs with holes
discs = []
for pos in [(-10, 0, 0), (2, 0, 0)]:
    d = (
        cq.Workplane("YZ", origin=pos)
        .circle(disc_radius)
        .extrude(disc_thickness)
        .faces("<X")
        .workplane()
        .pushPoints(disc_hole_radius_positions)
        .hole(disc_hole_diameter, disc_hole_depth)
    )
    discs.append(d)
disc1, disc2 = discs

# Shaft cylinder
shaft = (
    cq.Workplane("YZ", origin=(shaft_start, 0, 0))
    .circle(shaft_radius)
    .extrude(shaft_length)
)

# Nozzle by lofting two circles
nozzle = (
    cq.Workplane("YZ", origin=(nozzle_start, 0, 0))
    .circle(nozzle_base_radius)
    .workplane(offset=nozzle_length)
    .circle(nozzle_tip_radius)
    .loft()
)

# Combine all parts
result = plate.union(supports).union(disc1).union(disc2).union(shaft).union(nozzle)