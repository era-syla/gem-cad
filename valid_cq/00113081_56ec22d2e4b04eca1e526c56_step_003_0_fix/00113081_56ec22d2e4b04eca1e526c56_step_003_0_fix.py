import cadquery as cq
import math

# Parameters
t = 2.0
R = 20.0
hole_dia = 5.0
slot_w = 8.0
slot_l = 30.0

# Points for three slots around the circle
points = [
    ((R * 0.7) * math.cos(math.radians(a)), (R * 0.7) * math.sin(math.radians(a)))
    for a in (0, 120, 240)
]

# Circular part with central hole and three slots
circular = (
    cq.Workplane("XY")
    .circle(R)
    .extrude(t)
    .faces(">Z")
    .workplane()
    .hole(hole_dia)
    .faces(">Z")
    .workplane()
    .pushPoints(points)
    .rect(slot_w, slot_l)
    .cutThruAll()
)

# Bar part parameters
length = 80.0
width = 12.0

bar = (
    cq.Workplane("XY")
    .moveTo(60, 0)
    .rect(length, width)
    .extrude(t)
)

# Add curled loops at each corner of the bar
loop_r = 5.0
for x0 in (60 - length/2, 60 + length/2):
    for y0 in ( width/2, -width/2):
        bar = bar.union(
            cq.Workplane("YZ")
            .transformed(offset=(x0, y0, 0))
            .rect(t, 2 * loop_r)
            .revolve(360, (x0, y0, 0), (x0 + 1, y0, 0))
        )

# Combine both parts
result = circular.union(bar)