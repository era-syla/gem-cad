import cadquery as cq

# Main block (left part - slide block)
left_block = (
    cq.Workplane("XY")
    .box(60, 40, 20)
)

# Add a rail slot on bottom of left block
left_block = (
    left_block
    .faces(">Z")
    .workplane()
    .center(0, -15)
    .rect(50, 8)
    .cutBlind(-5)
)

# Add mounting holes to left block top face
left_block = (
    left_block
    .faces(">Z")
    .workplane()
    .pushPoints([(-15, 5), (15, 5), (0, -5)])
    .circle(3)
    .cutBlind(-10)
)

# Add hex pocket on top
left_block = (
    left_block
    .faces(">Z")
    .workplane()
    .center(0, 10)
    .polygon(6, 8)
    .cutBlind(-4)
)

# Right block (bracket with clevis)
right_block = (
    cq.Workplane("XY")
    .box(50, 40, 40)
    .translate((65, 0, 10))
)

# Cut center slot for clevis on front face
right_block = (
    right_block
    .faces(">X")
    .workplane()
    .center(0, 5)
    .rect(16, 20)
    .cutBlind(-30)
)

# Add clevis pin hole through the sides
right_block = (
    right_block
    .faces(">Y")
    .workplane()
    .center(0, 5)
    .circle(5)
    .cutThruAll()
)

# Add mounting holes on right block top
right_block = (
    right_block
    .faces(">Z")
    .workplane()
    .pushPoints([(-10, 10), (10, 10)])
    .circle(3)
    .cutBlind(-15)
)

# Add side holes on right block
right_block = (
    right_block
    .faces(">X")
    .workplane()
    .pushPoints([(10, -10), (-10, -10), (10, -20), (-10, -20)])
    .circle(2.5)
    .cutBlind(-10)
)

# Create the clevis/pulley wheel
clevis_wheel = (
    cq.Workplane("YZ")
    .center(0, 25)
    .circle(9)
    .extrude(6)
    .translate((65, 0, 10))
)

# Inner bore of wheel
clevis_wheel = (
    clevis_wheel
    .faces(">X")
    .workplane()
    .circle(4)
    .cutThruAll()
)

# Groove on wheel
clevis_wheel = (
    clevis_wheel
    .faces(">X")
    .workplane()
    .circle(7)
    .circle(9)
    .cutBlind(-2)
)

# Left block lower rail/guide
left_guide = (
    cq.Workplane("XY")
    .box(60, 10, 8)
    .translate((0, -25, -14))
)

# Right block lower flange
right_flange = (
    cq.Workplane("XY")
    .box(10, 40, 40)
    .translate((90, 0, 10))
)

# Add holes to right flange
right_flange = (
    right_flange
    .faces(">X")
    .workplane()
    .pushPoints([(10, 10), (10, -10), (-10, 10), (-10, -10)])
    .circle(2.5)
    .cutBlind(-8)
)

# Combine all parts
result = (
    left_block
    .union(right_block)
    .union(clevis_wheel)
    .union(left_guide)
    .union(right_flange)
)