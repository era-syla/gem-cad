import cadquery as cq

# Parameters
thickness = 5
Rhub_in = 8
Rhub_out = 15
Rout_in = 12
Rout_out = 20
Rout_center = 40
Rrod = 3
Rrod_center = (Rhub_out + Rout_center) / 2

# Create central hub with bore
result = (
    cq.Workplane("XY")
    .circle(Rhub_out)
    .circle(Rhub_in)
    .extrude(thickness)
)

# Add four outer rings
for angle in [0, 90, 180, 270]:
    result = result.union(
        cq.Workplane("XY")
        .transformed(rotate=(0, 0, angle))
        .workplane()
        .center(Rout_center, 0)
        .circle(Rout_out)
        .circle(Rout_in)
        .extrude(thickness)
    )

# Add connecting rods between hub and outer rings
for angle in [45, 135, 225, 315]:
    result = result.union(
        cq.Workplane("XY")
        .transformed(rotate=(0, 0, angle))
        .workplane()
        .center(Rrod_center, 0)
        .circle(Rrod)
        .extrude(thickness)
    )

# Final result
result  # contains the assembled solid geometry