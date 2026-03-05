import cadquery as cq

thk = 2.0

# Central panel
result = cq.Workplane("XY").rect(120, 40).extrude(thk)

# Right panel
right_panel = (
    cq.Workplane("XY")
    .rect(60, 40)
    .extrude(thk)
    .translate((90, 0, 0))
    .rotate((60, -20, 0), (60, 20, 0), 90)
)
result = result.union(right_panel)

# Left panel
left_panel = (
    cq.Workplane("XY")
    .rect(60, 40)
    .extrude(thk)
    .translate((-90, 0, 0))
    .rotate((-60, 20, 0), (-60, -20, 0), 90)
)
result = result.union(left_panel)

# Top panel
top_panel = (
    cq.Workplane("XY")
    .rect(120, 40)
    .extrude(thk)
    .translate((0, 30, 0))
    .rotate((60, 20, 0), (-60, 20, 0), -90)
)
result = result.union(top_panel)

# Bottom panel
bottom_panel = (
    cq.Workplane("XY")
    .rect(120, 40)
    .extrude(thk)
    .translate((0, -30, 0))
    .rotate((-60, -20, 0), (60, -20, 0), -90)
)
result = result.union(bottom_panel)