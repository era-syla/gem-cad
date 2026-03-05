import cadquery as cq

# Parameters for the wheel
outer_r = 40
inner_r = 30
thickness = 12
rib_w = 4
rib_l = outer_r - inner_r

# Build the hollow wheel shell
wheel = cq.Workplane("XY") \
    .circle(outer_r) \
    .circle(inner_r) \
    .extrude(thickness)

# Add four radial ribs
for angle in [0, 45, 90, 135]:
    rib = (
        cq.Workplane("XY")
        .center(inner_r + rib_l/2, 0)
        .rect(rib_l, rib_w)
        .extrude(thickness)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    wheel = wheel.union(rib)

# Build the tapered bracket
bracket = (
    cq.Workplane("XZ")
    .polyline([(0, 0), (20, 0), (15, 60), (0, 60)])
    .close()
    .extrude(-15)
    .faces(">Y")
    .workplane()
    .pushPoints([(10, 15), (10, 30), (10, 45)])
    .polygon(6, 8)
    .cutThruAll()
)

# Combine both parts into the final result
result = cq.Workplane("XY").add(wheel).add(bracket)