import cadquery as cq
import math

# Build a bicycle crankset (crank arm + chainrings + spindle) and a pedal

# ── helpers ──────────────────────────────────────────────────────────────────

def make_chainring(od, id_, tooth_h=1.8, tooth_w=1.2, n_teeth=None, thickness=2.5):
    """Flat annular disc with simple rectangular teeth on the outside."""
    if n_teeth is None:
        n_teeth = int(math.pi * od / (tooth_w * 2.2))
    ring = (
        cq.Workplane("XY")
        .circle(od / 2 + tooth_h)
        .circle(id_ / 2)
        .extrude(thickness)
    )
    # cut tooth gaps around the perimeter
    gap_angle = 360.0 / n_teeth
    gap_w = tooth_w * 0.9
    gap_cutter = (
        cq.Workplane("XY")
        .rect(gap_w, tooth_h * 2 + 2)
        .extrude(thickness + 2)
    )
    for i in range(n_teeth):
        angle = i * gap_angle
        rad = math.radians(angle)
        cx = math.cos(rad) * (od / 2 + tooth_h)
        cy = math.sin(rad) * (od / 2 + tooth_h)
        cutter = gap_cutter.rotate((0, 0, 0), (0, 0, 1), angle)
        cutter = cutter.translate((cx, cy, -1))
        ring = ring.cut(cutter)
    return ring

def make_lightening_holes(solid, n=5, r_pos=None, hole_r=4.0):
    """Cut n evenly-spaced lightening holes into a ring solid."""
    for i in range(n):
        angle = math.radians(i * 360.0 / n)
        cx = math.cos(angle) * r_pos
        cy = math.sin(angle) * r_pos
        cutter = (
            cq.Workplane("XY")
            .transformed(offset=cq.Vector(cx, cy, -1))
            .circle(hole_r)
            .extrude(20)
        )
        solid = solid.cut(cutter)
    return solid

# ── spindle / bottom-bracket axle ────────────────────────────────────────────
spindle = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0, -45))
    .circle(7)
    .extrude(90)
)

# ── crank arm ────────────────────────────────────────────────────────────────
arm_len = 95
arm_w   = 14
arm_t   = 9

crank_arm = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(arm_len / 2, 0, -arm_t / 2))
    .box(arm_len, arm_w, arm_t)
)

# round the far end (pedal boss)
pedal_boss = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(arm_len, 0, 0))
    .circle(arm_w / 2)
    .extrude(arm_t)
    .translate((0, 0, -arm_t / 2))
)

# round the near end (BB boss)
bb_boss = (
    cq.Workplane("XY")
    .circle(arm_w / 2 + 2)
    .extrude(arm_t)
    .translate((0, 0, -arm_t / 2))
)

crank_arm = crank_arm.union(pedal_boss).union(bb_boss)

# pedal axle stub
pedal_stub = (
    cq.Workplane("YZ")
    .transformed(offset=cq.Vector(0, 0, arm_len))
    .circle(5)
    .extrude(18)
)

# ── chainrings ────────────────────────────────────────────────────────────────
# large ring
ring_large = make_chainring(od=74, id_=30, thickness=2.5, n_teeth=38)
ring_large = make_lightening_holes(ring_large, n=5, r_pos=22, hole_r=5)
ring_large = ring_large.translate((0, 0, 2))

# small ring
ring_small = make_chainring(od=54, id_=26, thickness=2.4, n_teeth=28)
ring_small = make_lightening_holes(ring_small, n=5, r_pos=17, hole_r=3.5)
ring_small = ring_small.translate((0, 0, -4))

# ── assemble crankset ─────────────────────────────────────────────────────────
crankset = (
    spindle
    .union(crank_arm)
    .union(pedal_stub)
    .union(ring_large)
    .union(ring_small)
)

# ── simple pedal body ─────────────────────────────────────────────────────────
pedal_body = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0, -8))
    .box(70, 28, 16)
)

# pedal cage sides
for sx in [-1, 1]:
    rib = (
        cq.Workplane("XZ")
        .transformed(offset=cq.Vector(0, sx * 14, 0))
        .rect(70, 16)
        .extrude(2)
        .translate((0, 0, -8))
    )
    pedal_body = pedal_body.union(rib)

# pedal spindle hole
pedal_spindle_hole = (
    cq.Workplane("XY")
    .circle(5.2)
    .extrude(30)
    .translate((0, 0, -15))
)
pedal_body = pedal_body.cut(pedal_spindle_hole)

# position the pedal away from the crankset
pedal = pedal_body.translate((-160, 60, 10))

# ── final result ──────────────────────────────────────────────────────────────
result = crankset.union(pedal)