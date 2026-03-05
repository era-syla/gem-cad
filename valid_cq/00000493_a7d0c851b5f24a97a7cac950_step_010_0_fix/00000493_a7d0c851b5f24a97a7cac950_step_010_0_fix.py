import cadquery as cq

# Main cylinder (tube body)
outer_radius = 15
inner_radius = 12
tube_length = 80

# Create main tube
tube = (
    cq.Workplane("YZ")
    .circle(outer_radius)
    .extrude(tube_length)
)

# Hollow out the tube
tube = (
    tube
    .faces(">X")
    .workplane()
    .circle(inner_radius)
    .cutBlind(-tube_length + 5)
)

# Front flange (larger ring at the front)
flange_outer = 20
flange_inner = 13
flange_thickness = 6

flange = (
    cq.Workplane("YZ")
    .circle(flange_outer)
    .extrude(flange_thickness)
)

# Hollow out flange
flange = (
    flange
    .faces(">X")
    .workplane()
    .circle(flange_inner)
    .cutBlind(-flange_thickness)
)

# Combine tube and flange
body = tube.union(flange)

# Add a small knob/screw on the side of the flange area
knob = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(3, -flange_outer, 0))
    .circle(2)
    .extrude(5)
)

body = body.union(knob)

# Add rack gear on top of tube (simplified as a rectangular bar with notches)
rack_length = 40
rack_width = 4
rack_height = 3

rack_base = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(tube_length - rack_length - 5, outer_radius, -rack_height/2))
    .rect(rack_length, rack_width)
    .extrude(rack_height)
)

# Add teeth to rack (simplified)
for i in range(10):
    tooth = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(tube_length - rack_length - 5 + i * 4 + 1, outer_radius + rack_width/2 - 0.5, -rack_height/2))
        .rect(2, 2)
        .extrude(rack_height + 1.5)
    )
    rack_base = rack_base.union(tooth)

body = body.union(rack_base)

# Add pinion gear shaft (small cylinder sticking out from side)
shaft = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(tube_length - rack_length/2 - 5, 0, outer_radius + rack_width + 2))
    .circle(2.5)
    .extrude(25)
)

body = body.union(shaft)

# Add small pinion gear (disk)
pinion = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(tube_length - rack_length/2 - 5, 0, outer_radius + rack_width))
    .circle(5)
    .extrude(4)
)

body = body.union(pinion)

# Add bottom support knob/foot
foot = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(5, 0, -flange_outer + 2))
    .circle(4)
    .extrude(6)
)

body = body.union(foot)

# Add small bolt/screw on the side of flange
bolt = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(2, flange_outer - 1, 3))
    .circle(1.5)
    .extrude(5)
)

body = body.union(bolt)

result = body