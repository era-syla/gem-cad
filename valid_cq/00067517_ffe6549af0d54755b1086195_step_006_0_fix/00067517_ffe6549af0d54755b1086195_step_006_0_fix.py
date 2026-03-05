import cadquery as cq

R_big = 5
R_small = 3
big_height = 60
small_top = 10
small_bottom = 10
nose_length = 20
nose_tip_radius = 0.1

# Build main shaft
result = (
    cq.Workplane("XY")
    .circle(R_big).extrude(big_height)
    .faces(">Z").workplane().circle(R_small).extrude(small_top)
    .faces("<Z").workplane().circle(R_small).extrude(-small_bottom)
)

# Build lateral nose by lofting circles in YZ planes (extrude along X)
mid_z = small_bottom + big_height / 2
nose = (
    cq.Workplane("YZ", origin=(0, 0, mid_z))
    .circle(R_big)
    .workplane(offset=nose_length)
    .circle(nose_tip_radius)
    .loft(combine=True)
)

result = result.union(nose)