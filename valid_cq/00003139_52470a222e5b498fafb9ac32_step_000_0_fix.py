import cadquery as cq

# Main bracket body (right side)
bracket_right = (
    cq.Workplane("XY")
    .box(20, 20, 20)
    .faces(">X")
    .workplane()
    .rect(8, 8)
    .cutThruAll()
)

# Add mounting tabs to bracket
bracket_right = (
    bracket_right
    .faces(">Z")
    .workplane()
    .center(-5, 0)
    .box(8, 20, 4, combine=True)
)

# Left bracket body
bracket_left = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-40, 0, 0))
    .box(20, 20, 20)
)

bracket_left = (
    bracket_left
    .faces(">X")
    .workplane()
    .rect(8, 8)
    .cutThruAll()
)

# Central roller/pulley assembly
roller = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-10, 0, 0))
    .cylinder(8, 10)
)

# Shaft through roller
shaft = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-10, 0, 0))
    .cylinder(4, 30)
)

# Flat plate/body in center
center_plate = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-10, 0, -2))
    .box(30, 15, 8)
)

# Slots in center plate
center_plate = (
    center_plate
    .faces(">Y")
    .workplane()
    .rarray(6, 1, 4, 1)
    .rect(2, 6)
    .cutThruAll()
)

# Rod/pin extending left
rod = (
    cq.Workplane("YZ")
    .transformed(offset=cq.Vector(0, -25, 0))
    .circle(3)
    .extrude(18)
)

# Small connector block
connector = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(15, -5, -2))
    .box(8, 6, 8)
)

# Hole in connector
connector = (
    connector
    .faces(">X")
    .workplane()
    .circle(2)
    .cutThruAll()
)

# Right bracket with holes
right_main = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(18, 0, 2))
    .box(18, 22, 22)
)

right_main = (
    right_main
    .faces(">X")
    .workplane()
    .circle(5)
    .cutThruAll()
)

right_main = (
    right_main
    .faces("<X")
    .workplane()
    .circle(5)
    .cutThruAll()
)

# Top tab on right bracket
right_tab = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(18, 0, 16))
    .box(18, 8, 6)
)

# Combine all parts
result = (
    bracket_right
    .union(bracket_left)
    .union(roller)
    .union(shaft)
    .union(center_plate)
    .union(rod)
    .union(connector)
    .union(right_main)
    .union(right_tab)
)