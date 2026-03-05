import cadquery as cq

# Parameters
L = 200        # total length
W = 25         # width
T = 3          # thickness
c = 7          # chamfer distance at ends
main_hole_d = 6
side_hole_d = 3
off_main = 20  # distance from tip to main hole
off_y = 8      # side hole offset from centerline

# Create 2D profile with chamfered ends
profile = (
    cq.Workplane("XY")
      .polyline([
          (-L/2 + c, -W/2),
          ( L/2 - c, -W/2),
          ( L/2    ,   0  ),
          ( L/2 - c,  W/2),
          (-L/2 + c,  W/2),
          (-L/2    ,   0  )
      ])
      .close()
)

# Extrude to get 3D plate
result = profile.extrude(T)

# Create holes on top face
wp = result.faces(">Z").workplane()

# Main center holes at both ends
main_pts = [
    ( L/2 - off_main, 0),
    (-L/2 + off_main, 0)
]
wp.pushPoints(main_pts).hole(main_hole_d)

# Side holes (two at each end)
side_pts = [
    ( L/2 - off_main,  off_y),
    ( L/2 - off_main, -off_y),
    (-L/2 + off_main,  off_y),
    (-L/2 + off_main, -off_y)
]
wp.pushPoints(side_pts).hole(side_hole_d)