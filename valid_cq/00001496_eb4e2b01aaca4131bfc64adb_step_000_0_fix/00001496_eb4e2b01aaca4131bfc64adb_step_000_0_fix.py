import cadquery as cq

# Parameters
base_len = 60
base_wid = 20
base_thk = 5
pocket_d = 10
pocket_depth = 2
hole_d = 4
vert_wid = 20
vert_thk = 5
vert_h = 40
slot_w_top = 15
slot_w_bot = 6
slot_d_top = 3
slot_d_bot = 7

# Build base plate
result = cq.Workplane("XY").box(base_len, base_wid, base_thk)

# Hexagonal pockets at the ends
pocket_x = base_len/2 - pocket_d/2 - 2
pocket_pts = [(-pocket_x, 0), (pocket_x, 0)]
result = result.faces(">Z").workplane().pushPoints(pocket_pts).polygon(6, pocket_d).cutBlind(-pocket_depth)

# Through holes at pocket centers
result = result.faces(">Z").workplane().pushPoints(pocket_pts).hole(hole_d)

# Vertical wall in center
result = result.faces(">Z").workplane().rect(vert_wid, vert_thk).extrude(vert_h)

# T-slot on top of the vertical wall
#   wide shallow cut
result = result.faces(">Z").workplane().rect(slot_w_top, vert_thk).cutBlind(-slot_d_top)
#   narrow deeper cut
result = result.faces(">Z").workplane().rect(slot_w_bot, vert_thk).cutBlind(-(slot_d_top + slot_d_bot))

# Two mounting holes in the vertical face
hole_positions = [(-vert_wid/4, 0), (vert_wid/4, 0)]
result = result.faces(">Y").workplane().pushPoints(hole_positions).hole(hole_d)