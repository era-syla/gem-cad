import cadquery as cq

# Parameters
bar_thickness = 5
bar_width = 20
horiz_len = 180
vert_len = 90
hole_d = 8
spacing = 30
edge_offset = 15
boss_d = 12
boss_h = 4

# Create horizontal bar
hbar = cq.Workplane("XY").rect(horiz_len, bar_width).extrude(bar_thickness)

# Create vertical bar at the right end of the horizontal bar
vbar = (
    cq.Workplane("XY")
    .rect(bar_width, vert_len)
    .extrude(bar_thickness)
    .translate((horiz_len / 2 - bar_width / 2, vert_len / 2, 0))
)

# Combine bars
result = hbar.union(vbar)

# Add through holes on horizontal bar
h_pts = [
    (-horiz_len / 2 + edge_offset + i * spacing, 0)
    for i in range(int((horiz_len - 2 * edge_offset) / spacing) + 1)
]
result = result.faces(">Z").workplane().pushPoints(h_pts).hole(hole_d)

# Add through holes on vertical bar
vx = horiz_len / 2 - bar_width / 2
v_pts = [
    (vx, edge_offset + i * spacing)
    for i in range(int((vert_len - 2 * edge_offset) / spacing) + 1)
]
result = result.faces(">Z").workplane().pushPoints(v_pts).hole(hole_d)

# Add boss at the elbow joint
result = (
    result.faces(">Z")
    .workplane()
    .center(vx, 0)
    .circle(boss_d / 2)
    .extrude(boss_h)
)