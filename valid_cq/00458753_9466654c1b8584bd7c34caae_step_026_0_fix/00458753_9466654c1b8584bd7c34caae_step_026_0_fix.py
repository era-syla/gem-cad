import cadquery as cq

# Parameters
plate_w = 80
plate_h = 60
plate_t = 5

tab_d = 12

corner_hole_d = 4
corner_offset = 5

pocket_w = 60
pocket_h = 40
pocket_depth = 2

inner_boss_w = 40
inner_boss_h = 20
boss_height = 3

cut_w = 8
cut_h = 12
cut_gap = 4

# Build base plate
result = cq.Workplane("XY").box(plate_w, plate_h, plate_t)

# Add left and right mounting tabs
result = result.union(
    cq.Workplane("XY")
      .transformed(offset=(-plate_w/2, 0, -plate_t/2))
      .circle(tab_d/2)
      .extrude(plate_t)
)
result = result.union(
    cq.Workplane("XY")
      .transformed(offset=( plate_w/2, 0, -plate_t/2))
      .circle(tab_d/2)
      .extrude(plate_t)
)

# Corner mounting holes
hole_positions = [
    ( plate_w/2 - corner_offset,  plate_h/2 - corner_offset),
    (-plate_w/2 + corner_offset,  plate_h/2 - corner_offset),
    (-plate_w/2 + corner_offset, -plate_h/2 + corner_offset),
    ( plate_w/2 - corner_offset, -plate_h/2 + corner_offset),
]
result = result.faces(">Z").workplane().pushPoints(hole_positions).hole(corner_hole_d)

# Pocket cut into top face
result = result.faces(">Z").workplane().rect(pocket_w, pocket_h).cutBlind(-pocket_depth)

# Inner boss on pocket bottom
result = result.workplane(offset=-pocket_depth).rect(inner_boss_w, inner_boss_h).extrude(boss_height)

# Rectangular cutouts through the boss only
x1 = -(cut_w/2 + cut_gap/2)
x2 =  (cut_w/2 + cut_gap/2)
cut_positions = [(x1, 0), (x2, 0)]
result = result.faces(">Z").workplane().pushPoints(cut_positions).rect(cut_w, cut_h).cutBlind(-boss_height)

# Fillet all vertical edges
result = result.edges("|Z").fillet(1)

# Final result
# result contains the solid
