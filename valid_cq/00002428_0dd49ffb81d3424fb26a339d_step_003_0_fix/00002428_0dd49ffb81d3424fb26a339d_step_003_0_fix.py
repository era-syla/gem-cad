import cadquery as cq

# Parameters
L = 80    # length in X
W = 30    # width in Y
H = 20    # height in Z
hole_d = 6.5
csk_d = 10
neck_depth = 2
neck_width = 6
body_depth = 5
body_width = 12

# Base block
block = cq.Workplane("XY").box(L, W, H)

# T‐slot profile points in local YZ plane
profile = [
    (-body_width/2, 0),
    ( body_width/2, 0),
    ( body_width/2, body_depth),
    ( neck_width/2, body_depth),
    ( neck_width/2, body_depth + neck_depth),
    (-neck_width/2, body_depth + neck_depth),
    (-neck_width/2, body_depth),
    (-body_width/2, body_depth),
]

# Bottom T‐slot (centered on Y=0)
slot_bottom = (
    cq.Workplane("YZ", origin=(-L/2, 0, 0))
      .polyline(profile)
      .close()
      .extrude(L + 1)
)
block = block.cut(slot_bottom)

# Side T‐slots at Y = +W/2 and Y = -W/2
slot_side_p = (
    cq.Workplane("YZ", origin=(-L/2, W/2, 0))
      .polyline(profile)
      .close()
      .extrude(L + 1)
)
slot_side_n = (
    cq.Workplane("YZ", origin=(-L/2, -W/2, 0))
      .polyline(profile)
      .close()
      .extrude(L + 1)
)
block = block.cut(slot_side_p).cut(slot_side_n)

# Countersunk holes on top face
hole_positions = [(-L/4, 0), (0, 0), (L/4, 0)]
result = (
    block.faces(">Z")
         .workplane()
         .pushPoints(hole_positions)
         .cskHole(hole_d, csk_d, H + 2)
)