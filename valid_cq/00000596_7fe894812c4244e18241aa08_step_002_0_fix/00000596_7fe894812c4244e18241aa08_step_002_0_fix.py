import cadquery as cq

# Create the main crankshaft assembly components

# 1. Piston (cylinder with slot)
piston = (
    cq.Workplane("XY")
    .cylinder(30, 20)
)
# Add slot cut to piston
piston = (
    piston
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(8, 25)
    .cutBlind(-15)
)
# Add small hole in piston
piston = (
    piston
    .faces(">X")
    .workplane()
    .center(0, 5)
    .circle(3)
    .cutThruAll()
)

# 2. Connecting rod
con_rod = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(8)
    .extrude(6)
    .faces(">Z")
    .workplane()
    .circle(8)
    .extrude(2)
)
# Create the rod body
rod_body = (
    cq.Workplane("XY")
    .box(8, 40, 6)
    .translate((0, 20, 3))
)
# Small end circle
small_end = (
    cq.Workplane("XY")
    .center(0, 40)
    .circle(6)
    .extrude(6)
)
con_rod = con_rod.union(rod_body).union(small_end)
# Add holes
con_rod = (
    con_rod
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(4)
    .cutThruAll()
)

# 3. Crankshaft - main shaft
crankshaft = (
    cq.Workplane("XY")
    .circle(18)
    .extrude(8)
)
# Add gear/flange ring
crankshaft = crankshaft.union(
    cq.Workplane("XY")
    .circle(22)
    .circle(18)
    .extrude(4)
)
# Add inner ring
crankshaft = crankshaft.union(
    cq.Workplane("XY")
    .workplane(offset=8)
    .circle(14)
    .extrude(4)
)
# Main shaft body
shaft = (
    cq.Workplane("XY")
    .workplane(offset=12)
    .circle(6)
    .extrude(60)
)
crankshaft = crankshaft.union(shaft)

# Add square section to shaft
square_section = (
    cq.Workplane("XY")
    .workplane(offset=20)
    .rect(10, 10)
    .extrude(12)
)
crankshaft = crankshaft.union(square_section)

# Add threaded end (approximated as cylinder with smaller diameter)
thread_end = (
    cq.Workplane("XY")
    .workplane(offset=55)
    .circle(4)
    .extrude(17)
)
crankshaft = crankshaft.union(thread_end)

# 4. End cap / bearing housing
end_cap = (
    cq.Workplane("XY")
    .circle(22)
    .extrude(8)
)
# Add inner ring detail
end_cap = end_cap.cut(
    cq.Workplane("XY")
    .workplane(offset=2)
    .circle(16)
    .extrude(4)
)
# Add center hole
end_cap = end_cap.cut(
    cq.Workplane("XY")
    .circle(6)
    .extrude(8)
)
# Add outer flange
end_cap = end_cap.union(
    cq.Workplane("XY")
    .circle(25)
    .circle(22)
    .extrude(3)
)

# Position components for assembly view
piston_positioned = piston.translate((-60, 60, 0))
con_rod_positioned = con_rod.translate((-10, 30, 0))
crankshaft_positioned = crankshaft.translate((0, 0, 0))
end_cap_positioned = end_cap.translate((85, -20, 0))

# Combine all parts
result = (
    piston_positioned
    .union(con_rod_positioned)
    .union(crankshaft_positioned)
    .union(end_cap_positioned)
)