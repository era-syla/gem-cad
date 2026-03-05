import cadquery as cq

# Parameters
pipe_radius = 8.0        # radius of the pipe being clamped
wall_thickness = 3.0     # thickness of the clamp wall
clamp_width = 20.0       # width of each clamp ring
gap_between = 6.0        # gap between the two clamp rings
total_width = 2 * clamp_width + gap_between

bolt_boss_r = 5.0        # outer radius of bolt boss
bolt_hole_r = 2.5        # bolt hole radius
bolt_boss_h = 4.0        # height of bolt boss above clamp

outer_radius = pipe_radius + wall_thickness

# Build left clamp ring (hollow cylinder, open bottom - C-shape wrapping around pipe)
# We'll make a solid outer cylinder and subtract the pipe bore
# The clamp wraps around the pipe - make it as a full ring for simplicity

# Create the main body as two cylindrical rings connected by a bridge
# Each ring: outer cylinder minus inner bore
# Oriented along X axis (pipe runs along X)

# Single ring solid
def make_ring(width):
    outer = (
        cq.Workplane("YZ")
        .circle(outer_radius)
        .extrude(width)
    )
    inner = (
        cq.Workplane("YZ")
        .circle(pipe_radius)
        .extrude(width)
    )
    ring = outer.cut(inner)
    return ring

ring1 = make_ring(clamp_width)
ring2 = make_ring(clamp_width)

# Position ring2 offset in X
ring2 = ring2.translate((clamp_width + gap_between, 0, 0))

# Combine rings
body = ring1.union(ring2)

# Add connecting bridge between the rings (top and bottom connecting blocks)
# Bridge on top
bridge_h = wall_thickness
bridge_w = outer_radius * 2
bridge_top = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, outer_radius - bridge_h/2, 0))
    .box(total_width, bridge_h, bridge_h, centered=(True, True, True))
)

# Actually, let's make a rectangular bridge at the top
bridge = (
    cq.Workplane("XY")
    .box(total_width, outer_radius * 2, wall_thickness, centered=(False, True, True))
    .translate((0, 0, outer_radius - wall_thickness/2))
)

body = body.union(bridge)

# Bottom bridge
bridge_bot = (
    cq.Workplane("XY")
    .box(total_width, outer_radius * 2, wall_thickness, centered=(False, True, True))
    .translate((0, 0, -(outer_radius - wall_thickness/2)))
)

body = body.union(bridge_bot)

# Cut out a hole in the bottom for pipe passage (the bottom opening)
bottom_slot = (
    cq.Workplane("XY")
    .box(total_width, pipe_radius * 2 - 2, wall_thickness * 2, centered=(False, True, True))
    .translate((0, 0, -(outer_radius)))
)
body = body.cut(bottom_slot)

# Add bolt boss on top center
boss_x = total_width / 2
boss = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(boss_x, 0, outer_radius))
    .circle(bolt_boss_r)
    .extrude(bolt_boss_h)
)
body = body.union(boss)

# Cut bolt hole through boss and body
bolt_hole = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(boss_x, 0, outer_radius + bolt_boss_h))
    .circle(bolt_hole_r)
    .extrude(outer_radius * 2 + bolt_boss_h, both=True)
)
body = body.cut(bolt_hole)

# Center the result
result = body.translate((- total_width / 2, 0, 0))