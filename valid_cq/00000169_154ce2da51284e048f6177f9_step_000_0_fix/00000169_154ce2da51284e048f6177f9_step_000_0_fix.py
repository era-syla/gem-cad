import cadquery as cq

# Build a toggle clamp assembly
# Main mounting plate
mounting_plate = (
    cq.Workplane("YZ")
    .rect(40, 50)
    .extrude(6)
)

# Holes in mounting plate
mounting_plate = (
    mounting_plate
    .faces(">X")
    .workplane()
    .pushPoints([(-12, 12), (-12, -12), (12, 12), (12, -12)])
    .circle(3)
    .cutThruAll()
)

# Base body on top of mounting plate
base_body = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(35, 30)
    .extrude(20)
    .translate((10, 0, 0))
)

# Combine mounting plate and base
result = mounting_plate.union(base_body)

# Pivot arm body
pivot_arm = (
    cq.Workplane("XY")
    .center(10, 0)
    .rect(8, 25)
    .extrude(60)
    .translate((0, 0, 10))
)

result = result.union(pivot_arm)

# Handle arm
handle_arm = (
    cq.Workplane("XZ")
    .center(25, 20)
    .rect(8, 50)
    .extrude(8)
)

result = result.union(handle_arm)

# Handle ball
handle_ball = (
    cq.Workplane("XY")
    .center(60, 0)
    .sphere(10)
    .translate((0, 0, 20))
)

result = result.union(handle_ball)

# Top clamp bar
clamp_bar = (
    cq.Workplane("XY")
    .center(10, 0)
    .rect(8, 35)
    .extrude(8)
    .translate((0, 0, 65))
)

result = result.union(clamp_bar)

# Top clamp jaw
clamp_jaw = (
    cq.Workplane("YZ")
    .center(0, 69)
    .rect(30, 8)
    .extrude(20)
    .translate((0, 0, 0))
)

result = result.union(clamp_jaw)

# Pivot pin horizontal
pivot_pin1 = (
    cq.Workplane("XY")
    .center(10, 0)
    .circle(4)
    .extrude(40)
    .rotate((0, 0, 0), (0, 0, 1), 90)
    .translate((10, 0, 30))
)

result = result.union(pivot_pin1)

# Pivot pin for top
pivot_pin2 = (
    cq.Workplane("XY")
    .center(10, 0)
    .circle(4)
    .extrude(40)
    .rotate((0, 0, 0), (0, 0, 1), 90)
    .translate((10, 0, 65))
)

result = result.union(pivot_pin2)

# Adjustment rod
adj_rod = (
    cq.Workplane("XY")
    .center(10, 0)
    .circle(2.5)
    .extrude(30)
    .translate((0, 15, 65))
)

result = result.union(adj_rod)

# Small connecting pin
conn_pin = (
    cq.Workplane("YZ")
    .center(0, 35)
    .circle(3)
    .extrude(15)
    .translate((5, 0, 0))
)

result = result.union(conn_pin)

# Side mounting bolts
for y_pos in [-12, 0, 12]:
    bolt = (
        cq.Workplane("YZ")
        .center(y_pos, 25)
        .circle(3.5)
        .extrude(10)
        .translate((-5, 0, 0))
    )
    result = result.union(bolt)