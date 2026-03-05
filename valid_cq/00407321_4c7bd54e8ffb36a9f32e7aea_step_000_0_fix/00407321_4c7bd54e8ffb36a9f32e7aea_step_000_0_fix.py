import cadquery as cq

# Parameters
base_len = 80.0
base_wid = 10.0
thk = 2.0
flange_h = 12.0

stem_len = 6.0
stem_wid = 3.0
circle_r = 3.0

arrow_stem_w = 3.0
arrow_stem_h = 15.0
arrow_head_w = 10.0
arrow_head_h = 6.0

# Base plate
result = cq.Workplane("XY").box(base_len, base_wid, thk)

# Vertical flange on one long edge
flange = (
    cq.Workplane("XY")
    .workplane(offset=thk)
    .rect(base_len, thk)
    .extrude(flange_h)
    .translate((0.0, (base_wid + thk) / 2.0, 0.0))
)
result = result.union(flange)

# Left hook feature
left_hook = (
    cq.Workplane("XY")
    .workplane(offset=thk)
    .center(-base_len/2 + stem_len/2, 0)
    .rect(stem_len, stem_wid)
    .extrude(thk)
    .faces(">Z")
    .workplane()
    .circle(circle_r)
    .extrude(thk)
)
result = result.union(left_hook)

# Right hook feature
right_hook = (
    cq.Workplane("XY")
    .workplane(offset=thk)
    .center(base_len/2 - stem_len/2, 0)
    .rect(stem_len, stem_wid)
    .extrude(thk)
    .faces(">Z")
    .workplane()
    .circle(circle_r)
    .extrude(thk)
)
result = result.union(right_hook)

# Center arrow feature
arrow_profile = [
    (-arrow_stem_w/2, 0),
    ( arrow_stem_w/2, 0),
    ( arrow_stem_w/2, arrow_stem_h),
    ( arrow_head_w/2, arrow_stem_h),
    ( 0, arrow_stem_h + arrow_head_h),
    (-arrow_head_w/2, arrow_stem_h),
    (-arrow_stem_w/2, arrow_stem_h),
]
arrow = (
    cq.Workplane("XY")
    .workplane(offset=thk)
    .polyline(arrow_profile)
    .close()
    .extrude(thk)
)
result = result.union(arrow)