import cadquery as cq

# Parameters
base_length = 100
base_width = 40
base_th = 8
leg_depth = 20
leg_height = 60
small_hole = 4
large_hole = 20
pocket_depth = 6
fillet_radius = 4

# Base
result = cq.Workplane("XY").box(base_length, base_width, base_th)

# Front leg
result = result.union(
    cq.Workplane("XY")
      .transformed(offset=(-base_length/2 + leg_depth/2, 0, base_th/2))
      .box(leg_depth, base_width, leg_height)
)

# Back leg
result = result.union(
    cq.Workplane("XY")
      .transformed(offset=( base_length/2 - leg_depth/2, 0, base_th/2))
      .box(leg_depth, base_width, leg_height)
)

# U-shaped pocket from bottom
slot_length = base_length - 2*leg_depth
result = result.faces("<Z").workplane().center(0, 0).rect(slot_length, base_width).cutBlind(-pocket_depth)

# Fillet inner edges of the pocket
result = result.edges("|Z and (<Y or >Y)").fillet(fillet_radius)

# Small holes on top of base
result = result.faces(">Z").workplane().pushPoints([(-20, 0), (20, 0)]).hole(small_hole)

# Large hole in back leg
result = result.faces(">Y and >Z").workplane().hole(large_hole)

# Three small holes in front leg side face
result = result.faces("<Y and >Z").workplane().pushPoints([(0, -10), (0, 0), (0, 10)]).hole(small_hole)