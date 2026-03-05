import cadquery as cq

# Parameters
L = 80     # total length of the top bar
T = 10     # wall thickness (also thickness of top bar)
W = 5      # width (extrusion depth)
H_leg = 20 # height of the legs

# Build the top bar
bar = (
    cq.Workplane("XZ")
    .transformed(offset=(0, 0, H_leg))
    .rect(L, T)
    .extrude(W)
)

# Build the rectangular portions of the legs
left_leg_rect = (
    cq.Workplane("XZ")
    .transformed(offset=(-L/2 + T/2, 0, H_leg/2))
    .rect(T, H_leg)
    .extrude(W)
)
right_leg_rect = (
    cq.Workplane("XZ")
    .transformed(offset=( L/2 - T/2, 0, H_leg/2))
    .rect(T, H_leg)
    .extrude(W)
)

# Build the half‐cylinder end caps on the legs (full cylinders, the inner halves are covered by the leg rect)
R = H_leg / 2
left_leg_cyl = (
    cq.Workplane("XZ")
    .transformed(offset=(-L/2, 0, H_leg/2))
    .circle(R)
    .extrude(W)
)
right_leg_cyl = (
    cq.Workplane("XZ")
    .transformed(offset=( L/2, 0, H_leg/2))
    .circle(R)
    .extrude(W)
)

# Combine all parts
result = bar.union(left_leg_rect).union(right_leg_rect).union(left_leg_cyl).union(right_leg_cyl)