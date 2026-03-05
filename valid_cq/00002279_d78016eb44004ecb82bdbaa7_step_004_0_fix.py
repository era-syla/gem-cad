import cadquery as cq

# Part 1: Circular disc with slot hole
disc = (
    cq.Workplane("XY")
    .circle(40)
    .extrude(5)
)

# Add slot (elongated hole) to disc
slot_length = 18
slot_width = 8
disc = (
    disc
    .faces(">Z")
    .workplane()
    .center(-5, 0)
    .slot2D(slot_length, slot_width, 0)
    .cutThruAll()
)

# Add small hole to disc
disc = (
    disc
    .faces(">Z")
    .workplane()
    .center(15, 0)
    .circle(3)
    .cutThruAll()
)

# Part 2: Rectangular plate with large center hole and 4 corner holes
plate1 = (
    cq.Workplane("XY")
    .box(80, 40, 8)
)

# Large center hole
plate1 = (
    plate1
    .faces(">Z")
    .workplane()
    .circle(10)
    .cutThruAll()
)

# Corner holes
plate1 = (
    plate1
    .faces(">Z")
    .workplane()
    .rect(55, 20, forConstruction=True)
    .vertices()
    .circle(3)
    .cutThruAll()
)

# Part 3: Second rectangular plate (same as plate1 but positioned differently)
plate2 = (
    cq.Workplane("XY")
    .box(80, 40, 8)
)

# Large center hole
plate2 = (
    plate2
    .faces(">Z")
    .workplane()
    .circle(10)
    .cutThruAll()
)

# Corner holes
plate2 = (
    plate2
    .faces(">Z")
    .workplane()
    .rect(55, 20, forConstruction=True)
    .vertices()
    .circle(3)
    .cutThruAll()
)

# Position the parts separately in space
disc_positioned = disc.translate((-80, 30, 0))
plate1_positioned = plate1.translate((20, -20, 0))
plate2_positioned = plate2.translate((120, 20, 0))

# Combine all parts into result
result = (
    cq.Workplane("XY")
    .add(disc_positioned)
    .add(plate1_positioned)
    .add(plate2_positioned)
)