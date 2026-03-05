import cadquery as cq

# Parameters
pad_l = 30      # length of each end pad
bar_l = 140     # length of central bar
pad_w = 20      # width of each end pad
bar_w = 8       # width of central bar
t = 3           # plate thickness
k_d = 8         # knuckle diameter (also pin diameter)
k_r = k_d / 2   # knuckle radius
total_l = 2 * pad_l + bar_l
z0 = t + k_r    # vertical center of knuckles and pin

# Create the main plate with two pads and connecting bar
pts = [
    (-total_l/2,  pad_w/2),
    (-bar_l/2,    pad_w/2),
    (-bar_l/2,    bar_w/2),
    ( bar_l/2,    bar_w/2),
    ( bar_l/2,    pad_w/2),
    ( total_l/2,  pad_w/2),
    ( total_l/2, -pad_w/2),
    ( bar_l/2,   -pad_w/2),
    ( bar_l/2,   -bar_w/2),
    (-bar_l/2,   -bar_w/2),
    (-bar_l/2,   -pad_w/2),
    (-total_l/2, -pad_w/2),
]
plate = cq.Workplane("XY").polyline(pts).close().extrude(t)

# Left knuckle cylinder (leaf A)
knuckle1 = (
    cq.Workplane("YZ")
    .transformed(offset=(-bar_l/2 - k_r, 0, z0))
    .circle(k_r)
    .extrude(2 * k_r)
)

# Right knuckle cylinder (leaf B)
knuckle2 = (
    cq.Workplane("YZ")
    .transformed(offset=( bar_l/2 - k_r, 0, z0))
    .circle(k_r)
    .extrude(2 * k_r)
)

# Central pin cylinder
pin = (
    cq.Workplane("YZ")
    .transformed(offset=(-k_r, 0, z0))
    .circle(k_r)
    .extrude(2 * k_r)
)

# Combine all parts
result = plate.union(knuckle1).union(knuckle2).union(pin)