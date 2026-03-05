import cadquery as cq

# Parameters
L = 100      # Outer length in X
W = 80       # Outer width in Y
base_t = 2   # Base plate thickness
wall_h = 20  # Wall height
wall_t = 2   # Wall thickness
foot_d = 4   # Foot diameter
foot_h = 2   # Foot height
notch_w = 20 # Notch width in X
notch_h = 7  # Notch cut height from bottom

total_h = base_t + wall_h

# Build base plate
base = cq.Workplane("XY").box(L, W, base_t)

# Build walls as a rectangular ring extruded on top of the base
walls = (
    cq.Workplane("XY")
    .rect(L, W)
    .rect(L - 2 * wall_t, W - 2 * wall_t)
    .extrude(wall_h)
    .translate((0, 0, base_t))
)

# Combine base and walls
model = base.union(walls)

# Create notch cutting box and subtract
notch = (
    cq.Workplane("XY")
    .box(notch_w, wall_t * 2 + 0.1, notch_h)
    .translate((
        L / 2 - wall_t - notch_w / 2,      # X center of notch
        -W / 2 + wall_t / 2,               # Y center on front wall
        -total_h / 2 + notch_h / 2         # Z center from bottom
    ))
)
model = model.cut(notch)

# Add four cylindrical feet on the bottom corners
foot_r = foot_d / 2
corner_points = [
    ( L/2 - wall_t,  W/2 - wall_t),
    (-L/2 + wall_t,  W/2 - wall_t),
    ( L/2 - wall_t, -W/2 + wall_t),
    (-L/2 + wall_t, -W/2 + wall_t),
]
model = (
    model.faces("<Z")
    .workplane()
    .pushPoints(corner_points)
    .circle(foot_r)
    .extrude(foot_h)
)

result = model
