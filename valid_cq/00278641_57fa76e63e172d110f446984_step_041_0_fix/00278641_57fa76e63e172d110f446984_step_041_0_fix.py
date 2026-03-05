import cadquery as cq

# Parameters
thk = 5
r0 = 10       # bar half-width / left end radius
lead = 15
hole_spacing = 30
end_x = r0 + 2*lead + 2*hole_spacing  # total length from left circle center to right lobe centers
r_lobe = 7
offset = r0 + r_lobe  # vertical offset for the two right lobes
pos_large = [r0 + lead + hole_spacing*i for i in range(3)]
center = end_x/2
pos_large_cent = [(x - center, 0) for x in pos_large]
pos_small_cent = [(center,  offset), (center, -offset)]
D1 = 12  # large hole diameter
D2 = 6   # small hole diameter
r_boss = 8
h_boss = 2

# Base plate (rectangle)
plate = cq.Workplane("XY").rect(end_x, 2*r0).extrude(thk)

# Left semicircular end (full circle unioned)
left_end = cq.Workplane("XY").circle(r0).extrude(thk).translate((-center, 0, 0))

# Two right lobes
lobe_up = cq.Workplane("XY").circle(r_lobe).extrude(thk).translate((center,  offset, 0))
lobe_dn = cq.Workplane("XY").circle(r_lobe).extrude(thk).translate((center, -offset, 0))

# Fuse the shapes into one plate
result = plate.union(left_end).union(lobe_up).union(lobe_dn)

# Drill large holes through the bar
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(pos_large_cent)
    .hole(D1)
)

# Drill small holes in the right lobes
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(pos_small_cent)
    .hole(D2)
)

# Add a boss on the middle large hole
boss = (
    cq.Workplane("XY")
    .workplane(offset=thk)
    .center(pos_large_cent[1][0], 0)
    .circle(r_boss)
    .extrude(h_boss)
)
result = result.union(boss)