import cadquery as cq

# Build a simplified forklift model using basic geometric primitives

# Main body of the forklift
body = (
    cq.Workplane("XY")
    .box(60, 80, 50, centered=(True, True, False))
)

# Rounded front of body
body_front = (
    cq.Workplane("XY")
    .cylinder(50, 30)
    .translate((0, 40, 25))
)

# Combine body parts
forklift = body.union(body_front)

# Engine hood / rear counterweight (bulge at back)
counterweight = (
    cq.Workplane("XY")
    .box(60, 25, 45, centered=(True, True, False))
    .translate((0, -52, 0))
)
forklift = forklift.union(counterweight)

# Seat area
seat = (
    cq.Workplane("XY")
    .box(30, 35, 8, centered=(True, True, False))
    .translate((0, -10, 50))
)
forklift = forklift.union(seat)

# Engine cylinder (propane tank or engine cover)
engine_cyl = (
    cq.Workplane("XY")
    .cylinder(30, 15)
    .translate((0, -20, 65))
)
forklift = forklift.union(engine_cyl)

# Overhead guard posts (4 vertical pillars)
post_h = 55
post_w = 4

# Front left post
post_fl = (
    cq.Workplane("XY")
    .box(post_w, post_w, post_h, centered=(True, True, False))
    .translate((-25, 30, 50))
)
forklift = forklift.union(post_fl)

# Front right post
post_fr = (
    cq.Workplane("XY")
    .box(post_w, post_w, post_h, centered=(True, True, False))
    .translate((25, 30, 50))
)
forklift = forklift.union(post_fr)

# Rear left post
post_rl = (
    cq.Workplane("XY")
    .box(post_w, post_w, post_h, centered=(True, True, False))
    .translate((-25, -35, 50))
)
forklift = forklift.union(post_rl)

# Rear right post
post_rr = (
    cq.Workplane("XY")
    .box(post_w, post_w, post_h, centered=(True, True, False))
    .translate((25, -35, 50))
)
forklift = forklift.union(post_rr)

# Overhead guard top frame
guard_top = (
    cq.Workplane("XY")
    .box(60, 70, 3, centered=(True, True, False))
    .translate((0, -5, 105))
)
forklift = forklift.union(guard_top)

# Overhead guard grid - cross members X direction
for i in range(4):
    bar = (
        cq.Workplane("XY")
        .box(60, 2, 2, centered=(True, True, False))
        .translate((0, -30 + i * 18, 105))
    )
    forklift = forklift.union(bar)

# Overhead guard grid - cross members Y direction
for i in range(5):
    bar = (
        cq.Workplane("XY")
        .box(2, 70, 2, centered=(True, True, False))
        .translate((-24 + i * 12, -5, 105))
    )
    forklift = forklift.union(bar)

# Wheels - front large wheels
wheel_radius = 15
wheel_width = 12

# Front left wheel
wfl = (
    cq.Workplane("YZ")
    .cylinder(wheel_width, wheel_radius)
    .translate((-36, 25, wheel_radius))
)
forklift = forklift.union(wfl)

# Front right wheel
wfr = (
    cq.Workplane("YZ")
    .cylinder(wheel_width, wheel_radius)
    .translate((36, 25, wheel_radius))
)
forklift = forklift.union(wfr)

# Rear smaller wheels
wheel_radius_r = 10
wheel_width_r = 8

wrl = (
    cq.Workplane("YZ")
    .cylinder(wheel_width_r, wheel_radius_r)
    .translate((-34, -45, wheel_radius_r))
)
forklift = forklift.union(wrl)

wrr = (
    cq.Workplane("YZ")
    .cylinder(wheel_width_r, wheel_radius_r)
    .translate((34, -45, wheel_radius_r))
)
forklift = forklift.union(wrr)

# Mast assembly - two vertical channels
mast_h = 90
mast_w = 5

mast_l = (
    cq.Workplane("XY")
    .box(mast_w, mast_w, mast_h, centered=(True, True, False))
    .translate((-18, 42, 5))
)
forklift = forklift.union(mast_l)

mast_r = (
    cq.Workplane("XY")
    .box(mast_w, mast_w, mast_h, centered=(True, True, False))
    .translate((18, 42, 5))
)
forklift = forklift.union(mast_r)

# Mast cross bars
for i in range(4):
    mbar = (
        cq.Workplane("XY")
        .box(36, mast_w, 3, centered=(True, True, False))
        .translate((0, 42, 10 + i * 22))
    )
    forklift = forklift.union(mbar)

# Carriage / backrest for forks
carriage = (
    cq.Workplane("XY")
    .box(40, 4, 30, centered=(True, True, False))
    .translate((0, 45, 5))
)
forklift = forklift.union(carriage)

# Forks - two horizontal prongs
fork_length = 80
fork_h = 5
fork_w = 8

fork_l = (
    cq.Workplane("XY")
    .box(fork_w, fork_length, fork_h, centered=(True, True, False))
    .translate((-12, 45, 5))
)
forklift = forklift.union(fork_l)

fork_r = (
    cq.Workplane("XY")
    .box(fork_w, fork_length, fork_h, centered=(True, True, False))
    .translate((12, 45, 5))
)
forklift = forklift.union(fork_r)

result = forklift