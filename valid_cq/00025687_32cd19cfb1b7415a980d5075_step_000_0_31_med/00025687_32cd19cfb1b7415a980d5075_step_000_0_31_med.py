import cadquery as cq

# Base U-frame parameters
width = 20
height = 20
thickness = 2
leg_width = 3
crossbar_height = 3

# Base U-frame centered at (0,0) with Z from -1 to 1
u_frame = (cq.Workplane("XY")
           .box(width, height, thickness)
           .faces(">Z").workplane()
           .center(0, -1.5)
           .rect(width - 2 * leg_width, height - crossbar_height)
           .cutThruAll()
          )

# Right Bottom (U-frame with notches)
right_bottom = (u_frame
                .translate((20, 0, 0))
                .faces(">Z").workplane()
                .center(20, 8.5)
                .pushPoints([(-5, 0), (5, 0)])
                .rect(3, 3)
                .cutThruAll()
               )

# Right Top (Square plate with tabs)
right_top = (cq.Workplane("XY")
             .center(20, 25)
             .box(20, 20, thickness)
            )

tabs = (cq.Workplane("XY")
        .center(20, 25)
        .pushPoints([(-5, 11.5), (5, 11.5), (-5, -11.5), (5, -11.5)])
        .box(3, 3, thickness)
       )

right_top = right_top.union(tabs)

# Left Part (U-frame + Curved Backrest)
left_bottom = u_frame.translate((-20, 0, 0))

# Profile for the curved backrest
pts = [
    (10, 10), (10, 13), (6, 20), (9, 28), (4, 34),
    (0, 35), (-4, 34), (-9, 28), (-6, 20), (-10, 13), (-10, 10)
]

backrest = (cq.Workplane("XY")
            .center(-20, 0)
            .polyline(pts).close()
            .extrude(thickness / 2.0, both=True)
           )

# Fillet the outer edges of the backrest
backrest = backrest.edges("|Z").fillet(1.0)

# Square cutouts on the backrest
backrest = (backrest.faces(">Z").workplane()
            .pushPoints([(-5, 13), (5, 13)])
            .rect(3, 3)
            .cutThruAll()
           )

# Diamond cutouts
d1 = [(0, 16), (1.5, 23), (0, 30), (-1.5, 23)]
d2 = [(-4, 17), (-2.5, 23), (-4, 29), (-5.5, 23)]
d3 = [(4, 17), (5.5, 23), (4, 29), (2.5, 23)]

for d in [d1, d2, d3]:
    backrest = (backrest.faces(">Z").workplane()
                .polyline(d).close()
                .cutThruAll())

# Combine the left part pieces
left_part = left_bottom.union(backrest)

# Final assembled scene
result = left_part.union(right_bottom).union(right_top)