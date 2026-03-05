import cadquery as cq

# Parameters
beam_length = 160
beam_width = 20
beam_height = 15

plate_thick = 10
plate_height = 30

boss_r = 5
boss_l = 10

support_depth = 10
support_height = 5

cyl_length = 80
cyl_r = 10

# Base beam
beam = cq.Workplane("XY").box(beam_length, beam_width, beam_height)

# Triangular cutouts along the side
x_positions = [-60, -30, 0, 30, 60]
for x in x_positions:
    beam = beam.faces(">Y").workplane().transformed(offset=(x, 0, 0)) \
        .polyline([(-5, -5), (5, -5), (0, 5)]).close().cutThruAll()

# End plates
plate1 = cq.Workplane("YZ") \
    .transformed(offset=(beam_length/2 + plate_thick/2, 0, -beam_height/2 + plate_height/2)) \
    .rect(beam_width, plate_height).extrude(plate_thick)
plate2 = cq.Workplane("YZ") \
    .transformed(offset=(-beam_length/2 - plate_thick/2, 0, -beam_height/2 + plate_height/2)) \
    .rect(beam_width, plate_height).extrude(-plate_thick)

# Boss cylinders on the plates
boss1 = cq.Workplane("YZ") \
    .transformed(offset=(beam_length/2 + plate_thick + boss_l/2, 0, 0)) \
    .circle(boss_r).extrude(boss_l)
boss2 = cq.Workplane("YZ") \
    .transformed(offset=(-beam_length/2 - plate_thick - boss_l/2, 0, 0)) \
    .circle(boss_r).extrude(-boss_l)

# Simple supports under the cylinder
support1 = cq.Workplane("XY").box(support_depth, beam_width, support_height) \
    .translate((20, 0, beam_height/2 + support_height/2))
support2 = cq.Workplane("XY").box(support_depth, beam_width, support_height) \
    .translate((-20, 0, beam_height/2 + support_height/2))

# Main cylinder on top
cyl = cq.Workplane("YZ") \
    .transformed(offset=(-cyl_length/2, 0, beam_height/2 + support_height + cyl_r)) \
    .circle(cyl_r).extrude(cyl_length)

# Combine all parts
result = beam.union(plate1).union(plate2) \
    .union(boss1).union(boss2) \
    .union(support1).union(support2) \
    .union(cyl)