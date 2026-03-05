import cadquery as cq

# Dimensions
base_l = 100
base_w = 30
base_t1 = 4
base_t2 = 4
wall_t = 3

boss_dia = 16
hole_dia = 8
hole_dist = 70

tube_od = 18
tube_id = 14
tube_L = 150

# 1. Base Plate Background
wp = cq.Workplane("XY")
base = wp.slot2D(base_l, base_w, 90).extrude(base_t1)

# 2. Raised perimeter and bosses
raised_wp = cq.Workplane("XY").workplane(offset=base_t1)

# Perimeter Wall
perimeter = (
    raised_wp
    .slot2D(base_l, base_w, 90)
    .slot2D(base_l - 2 * wall_t, base_w - 2 * wall_t, 90)
    .extrude(base_t2)
)
base = base.union(perimeter)

# Top and Bottom Hole Bosses
bosses = (
    raised_wp
    .pushPoints([(0, hole_dist / 2), (0, -hole_dist / 2)])
    .circle(boss_dia / 2)
    .extrude(base_t2)
)
base = base.union(bosses)

# Center Boss
center_boss = raised_wp.circle(tube_od / 2 + 3).extrude(base_t2)
base = base.union(center_boss)

# Bridge connecting center to hole bosses
bridge = raised_wp.rect(8, hole_dist).extrude(base_t2)
base = base.union(bridge)

# 3. Central Extruded Tube
tube = (
    cq.Workplane("XY")
    .workplane(offset=base_t1 + base_t2)
    .circle(tube_od / 2)
    .extrude(tube_L - (base_t1 + base_t2))
)
base = base.union(tube)

# 4. Gusset (Support Rib)
# YZ plane mapping: X corresponds to global Y, Y corresponds to global Z
gusset_pts = [
    (tube_od / 2, base_t1 + base_t2),                     # Bottom corner on center boss
    (tube_od / 2, 50),                                    # Top corner on the tube
    (hole_dist / 2 - boss_dia / 2 + 2, base_t1 + base_t2) # Bottom corner on the top boss
]

gusset = cq.Workplane("YZ").polyline(gusset_pts).close().extrude(2, both=True)
base = base.union(gusset)

# 5. Tab at the tip of the tube
tab_z = tube_L - 4
tab = (
    cq.Workplane("XY")
    .workplane(offset=tab_z)
    .center(0, -tube_od / 2 - 0.5)
    .rect(4, 3)
    .extrude(4)
)
base = base.union(tab)

# 6. Drilling Cuts
# Cut top and bottom mounting holes
base = base.cut(
    cq.Workplane("XY")
    .pushPoints([(0, hole_dist / 2), (0, -hole_dist / 2)])
    .circle(hole_dia / 2)
    .extrude(tube_L + 10)
)

# Cut central tube hole
base = base.cut(
    cq.Workplane("XY")
    .circle(tube_id / 2)
    .extrude(tube_L + 10)
)

# Optional: Add small fillets for realism
try:
    base = base.edges(">Z and (not %LINE)").fillet(1)
except Exception:
    pass

result = base