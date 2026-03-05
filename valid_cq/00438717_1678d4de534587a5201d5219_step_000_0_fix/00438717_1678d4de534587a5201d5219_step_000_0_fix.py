import cadquery as cq

# Parameters
d1 = 4.0   # diameter of left stub
d2 = 8.0   # diameter of mid shaft
d3 = 12.0  # diameter of right stub
l1 = 20.0  # length of left stub
l2 = 60.0  # length of mid shaft
l3 = 20.0  # length of right stub

stub1_count = 2
stub3_count = 3
groove_depth = 1.0
groove_width = 1.0

# Build the basic stepped shaft
result = cq.Workplane("XY") \
    .circle(d1/2).extrude(l1) \
    .workplane(offset=l1).circle(d2/2).extrude(l2) \
    .workplane(offset=l1 + l2).circle(d3/2).extrude(l3)

# Create grooves on left stub
for i in range(stub1_count):
    zpos = l1 * (i + 1) / (stub1_count + 1)
    outer_r = d1/2
    inner_r = outer_r - groove_depth
    cutter = (
        cq.Workplane("YZ", origin=(0, 0, zpos))
        .circle(outer_r)
        .circle(inner_r)
        .extrude(d3, both=True)
    )
    result = result.cut(cutter)

# Create grooves on right stub
for i in range(stub3_count):
    zpos = l1 + l2 + l3 * (i + 1) / (stub3_count + 1)
    outer_r = d3/2
    inner_r = outer_r - groove_depth
    cutter = (
        cq.Workplane("YZ", origin=(0, 0, zpos))
        .circle(outer_r)
        .circle(inner_r)
        .extrude(d3, both=True)
    )
    result = result.cut(cutter)