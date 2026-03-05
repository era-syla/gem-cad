import cadquery as cq

# Parameters
thk = 3
headR = 15
barW = 10
Lbar = 120
padW = 30
padL = 30

# Create head circle
head = cq.Workplane("XY").circle(headR).extrude(thk)

# Create rectangular bar
bar = (
    cq.Workplane("XY")
    .rect(Lbar, barW)
    .translate((headR + Lbar/2, 0, 0))
    .extrude(thk)
)

# Create trapezoidal pad
pts = [
    (headR + Lbar,  barW/2),
    (headR + Lbar + padL,  padW/2),
    (headR + Lbar + padL, -padW/2),
    (headR + Lbar, -barW/2),
]
pad = cq.Workplane("XY").polyline(pts).close().extrude(thk)

# Combine solids
result = head.union(bar).union(pad)

# Add holes on top face
# Head concentric holes
wp = result.faces(">Z").workplane()
wp = wp.hole(8).hole(4)

# Bar centerline holes
bar_hole_points = [(headR + 30, 0), (headR + 60, 0), (headR + 90, 0)]
wp = wp.pushPoints(bar_hole_points).hole(3)

# Pad corner holes
offset = 5
pad_hole_pts = [
    (headR + Lbar + offset,           padW/2 - offset),
    (headR + Lbar + padL - offset,    padW/2 - offset),
    (headR + Lbar + padL - offset,   -(padW/2 - offset)),
    (headR + Lbar + offset,          -(padW/2 - offset)),
]
wp = wp.pushPoints(pad_hole_pts).hole(3)

# Pad center hole
center_pt = (headR + Lbar + padL/2, 0)
result = wp.pushPoints([center_pt]).hole(5)

# 'result' now holds the final geometry.