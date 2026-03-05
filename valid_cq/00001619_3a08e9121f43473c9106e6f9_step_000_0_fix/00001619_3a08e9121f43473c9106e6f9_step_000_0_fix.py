import cadquery as cq

# Parameters
L = 120             # total main shaft length for extrusion
R_main = 6          # main journal radius
R_rod = 4           # rod journal radius
R_counter = 8       # counterweight radius
R_end = 8           # end boss radius
rod_positions = [-30, -10, 10, 30]
counter_offset = -10  # offset for counterweights
rod_length = 20
boss_length = 10

# Build main shaft (constant-radius cylinder)
result = cq.Workplane("YZ").circle(R_main).extrude(L, both=True)

# Add rod journals and counterweights
for x in rod_positions:
    # rod journal
    result = result.union(
        cq.Workplane("YZ")
        .transformed(offset=(x, 0, 0))
        .circle(R_rod)
        .extrude(rod_length, both=True)
    )
    # counterweight opposite the rod journal
    result = result.union(
        cq.Workplane("YZ")
        .transformed(offset=(x, counter_offset, 0))
        .circle(R_counter)
        .extrude(rod_length, both=True)
    )

# Add bosses at shaft ends
for x in (L/2 + boss_length/2, -L/2 - boss_length/2):
    result = result.union(
        cq.Workplane("YZ")
        .transformed(offset=(x, 0, 0))
        .circle(R_end)
        .extrude(boss_length, both=True)
    )