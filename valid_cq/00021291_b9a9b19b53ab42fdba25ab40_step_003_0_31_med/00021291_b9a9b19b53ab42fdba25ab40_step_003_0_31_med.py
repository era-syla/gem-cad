import cadquery as cq

# Parameters
L = 100.0          # Total length
H = 60.0           # Total height
D = 20.0           # Depth/thickness
F_H = 10.0         # Flange height
T_L = 24.0         # Top width
C_W = 12.0         # Channel width
C_D = 10.0         # Channel depth
hole_d = 5.0       # Hole diameter
hole_start_y = 15.0
hole_spacing = 9.5

# Define the points for the main profile
pts = [
    (-L/2, 0),
    (-L/2, F_H),
    (-T_L/2, H),
    (T_L/2, H),
    (L/2, F_H),
    (L/2, 0)
]

# Create the main extruded body
base = cq.Workplane("XY").polyline(pts).close().extrude(D)

# Create the bounding box for the channel and subtract it
channel = (
    cq.Workplane("XY")
    .workplane(offset=D - C_D/2.0)
    .center(0, H/2.0)
    .box(C_W, H + 10, C_D)  # Make height slightly larger to ensure clean cut
)
result = base.cut(channel)

# Add the 5 through-holes
for i in range(5):
    y_pos = hole_start_y + i * hole_spacing
    hole = (
        cq.Workplane("XY")
        .workplane(offset=-5)
        .center(0, y_pos)
        .circle(hole_d/2.0)
        .extrude(D + 10)
    )
    result = result.cut(hole)