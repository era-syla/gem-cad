import cadquery as cq

# Parametric dimensions based on visual proportions
L = 100         # Overall length
W = 40          # Overall width
H = 20          # Overall height
T = 3           # Wall thickness
R = 5           # Outer corner radius
W_front = 70    # Width of the opening at the front outer face
G = 60          # Gap between the inner hook tips
eps = 0.01      # Small epsilon for robust boolean operations

# 1. Base floor plate
floor = cq.Workplane("XY").box(L, W, T).edges("|Z").fillet(R)
# Shift so bottom rests at z = 0
floor = floor.translate((0, 0, T / 2))

# 2. Main walls
wall_h = H - T + eps
outer_wall = cq.Workplane("XY").box(L, W, wall_h).edges("|Z").fillet(R)
inner_wall = cq.Workplane("XY").box(L - 2 * T, W - 2 * T, wall_h).edges("|Z").fillet(max(0.1, R - T))
walls = outer_wall.cut(inner_wall)

# Translate walls upwards to sit exactly on top of the floor (with tiny overlap)
shift_z = (H + T - eps) / 2
walls = walls.translate((0, 0, shift_z))

# 3. Create a cutter for the front snap-fit opening
# The cut removes a trapezoidal prism from the front wall.
# We calculate extended points to ensure the cutter completely slices through the wall thickness.
K = (W_front - G) / (2 * T)
ext_y = 5.0  # Extension distance to ensure clean cuts

y_out = -W / 2 - ext_y
y_in = -W / 2 + T + ext_y

x_ol = -W_front / 2 - K * ext_y
x_or = W_front / 2 + K * ext_y
x_il = -G / 2 + K * ext_y
x_ir = G / 2 - K * ext_y

cut_pts = [
    (x_ol, y_out),
    (x_or, y_out),
    (x_ir, y_in),
    (x_il, y_in)
]

cutter = cq.Workplane("XY").polyline(cut_pts).close().extrude(H * 2)
# Center cutter vertically to guarantee it covers the wall height
cutter = cutter.translate((0, 0, -H / 2))

walls = walls.cut(cutter)

# 4. Final geometry: Union the floor and the cut walls
result = floor.union(walls)