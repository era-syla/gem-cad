import cadquery as cq

# Create individual components and combine them

# 1. Large spool/pulley (top right area)
spool_flange = (
    cq.Workplane("XY")
    .cylinder(4, 18)
)
spool_body = (
    cq.Workplane("XY")
    .cylinder(14, 12)
)
spool = spool_flange.union(spool_body)
# Add hole through spool
spool_hole = cq.Workplane("XY").cylinder(20, 4)
spool = spool.cut(spool_hole)
spool = spool.translate((40, 20, 0))

# 2. Washer next to spool
washer_outer = cq.Workplane("XY").cylinder(2, 12)
washer_hole = cq.Workplane("XY").cylinder(4, 6)
washer = washer_outer.cut(washer_hole)
washer = washer.translate((68, 18, 0))

# 3. Small bushings (middle area) - two of them
def make_bushing(inner_r=3, outer_r=7, flange_r=9, body_h=6, flange_h=2):
    body = cq.Workplane("XY").cylinder(body_h, outer_r)
    flange = cq.Workplane("XY").cylinder(flange_h, flange_r).translate((0, 0, body_h/2 - flange_h/2 + flange_h))
    bush = body.union(flange)
    hole = cq.Workplane("XY").cylinder(body_h + flange_h + 2, inner_r)
    bush = bush.cut(hole)
    return bush

bushing1 = make_bushing().translate((5, -5, 0))
bushing2 = make_bushing().translate((18, -5, 0))

# 4. Bolts/screws (long ones) - three of them
def make_bolt(shaft_r=3, head_r=6, head_h=4, shaft_h=35):
    shaft = cq.Workplane("XY").cylinder(shaft_h, shaft_r)
    head = cq.Workplane("XY").cylinder(head_h, head_r).translate((0, 0, shaft_h/2 + head_h/2))
    # Add small hole in head
    hole = cq.Workplane("XY").cylinder(head_h + 1, 2).translate((0, 0, shaft_h/2 + head_h/2))
    bolt = shaft.union(head).cut(hole)
    return bolt

bolt1 = make_bolt().translate((15, -25, 0))
bolt2 = make_bolt().translate((25, -28, 0))
bolt3 = make_bolt().translate((35, -25, 0))

# 5. Hex nut (bottom left)
def make_hex_nut(outer_d=10, inner_r=3.5, height=5):
    hex_body = cq.Workplane("XY").polygon(6, outer_d).extrude(height)
    hole = cq.Workplane("XY").cylinder(height + 1, inner_r)
    nut = hex_body.cut(hole)
    return nut

hex_nut = make_hex_nut().translate((-15, -15, 0))

# Combine all parts
result = spool.union(washer).union(bushing1).union(bushing2).union(bolt1).union(bolt2).union(bolt3).union(hex_nut)