import cadquery as cq

# Part 1
part1 = (
    cq.Workplane("XY")
    .box(60, 30, 10)
    .faces(">Z")
    .workplane()
    .hole(10)
    .faces(">Z")
    .workplane()
    .rect(50, 20)
    .cutBlind(-5)
)

# Part 2
part2 = (
    cq.Workplane("XY")
    .box(50, 40, 20)
    .faces(">Z")
    .workplane()
    .hole(12)
)

# Part 3
part3 = (
    cq.Workplane("XY")
    .box(40, 30, 15)
    .faces(">Z")
    .workplane()
    .rect(30, 20)
    .cutBlind(-10)
)

# Part 4
part4 = (
    cq.Workplane("XY")
    .box(20, 20, 20)
    .faces(">Z")
    .workplane()
    .hole(10)
)

# Part 5
part5 = (
    cq.Workplane("XY")
    .box(30, 30, 15)
    .faces(">Z")
    .workplane()
    .hole(8)
)

# Part 6
part6 = (
    cq.Workplane("XY")
    .box(20, 10, 5)
)

# Combine parts to make assembly (Mockup)
assembly = (
    part1.translate((0, 0, 0))
    .union(part2.translate((70, 0, 0)))
    .union(part3.translate((140, 0, 0)))
    .union(part4.translate((0, 50, 0)))
    .union(part5.translate((70, 50, 0)))
    .union(part6.translate((140, 50, 0)))
)

result = assembly
