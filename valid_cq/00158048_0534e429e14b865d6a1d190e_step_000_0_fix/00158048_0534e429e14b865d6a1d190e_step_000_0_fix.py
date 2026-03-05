import cadquery as cq

# Parameters
tip_d = 2
tip_len = 10
step1_d = 4
step1_len = 15
main_d = 8
main_len = 80
hub_d = 16
hub_thk = 8
hub_hole_d = 4

# Compute total length of shaft
half_total = tip_len * 2 + step1_len * 2 + main_len

# Build the stepped shaft centered at X=0
shaft = (
    cq.Workplane("YZ")
    .workplane(offset=-half_total/2)
    .circle(tip_d/2).extrude(tip_len)
    .faces(">X").workplane().circle(step1_d/2).extrude(step1_len)
    .faces(">X").workplane().circle(main_d/2).extrude(main_len)
    .faces(">X").workplane().circle(step1_d/2).extrude(step1_len)
    .faces(">X").workplane().circle(tip_d/2).extrude(tip_len)
)

# Build the central hub (disc) at the shaft center, extruded upward in +Y
disc = (
    cq.Workplane("XZ")
    .circle(hub_d/2)
    .extrude(hub_thk)
)

# Combine shaft and disc
result = shaft.union(disc)

# Drill a hole through the disc only
result = result.faces(">Y").workplane().hole(hub_hole_d, hub_thk)