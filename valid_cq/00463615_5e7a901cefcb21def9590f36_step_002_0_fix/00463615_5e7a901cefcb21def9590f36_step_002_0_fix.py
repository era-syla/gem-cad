import cadquery as cq

# Small fork with text
small_fork = (
    cq.Workplane("XY")
    .rect(24, 30)
    .extrude(3)
    .faces(">Z").workplane()
    .center(-10.5, -5)
    .rect(6, 20).cutThruAll()
    .center(21, 0)
    .rect(6, 20).cutThruAll()
    .faces(">Y").workplane()
    .text("stewle", 5, 1, cut=False)
)

# Middle plate with stud pattern
plate = (
    cq.Workplane("XY")
    .rect(24, 60)
    .extrude(3)
)
points = [(x, y) for x in (-5, 5) for y in (20, 10, 0, -10, -20, -30)]
plate = (
    plate
    .faces(">Z").workplane()
    .pushPoints(points)
    .circle(2)
    .extrude(1)
)

# Large fork
large_fork = (
    cq.Workplane("XY")
    .rect(24, 80)
    .extrude(3)
    .faces(">Z").workplane()
    .center(-10.5, 0)
    .rect(6, 60).cutThruAll()
    .center(21, 0)
    .rect(6, 60).cutThruAll()
)

# Assemble all parts
result = (
    small_fork.translate((-50, 0, 0))
    .union(plate)
    .union(large_fork.translate((50, 0, 0)))
)