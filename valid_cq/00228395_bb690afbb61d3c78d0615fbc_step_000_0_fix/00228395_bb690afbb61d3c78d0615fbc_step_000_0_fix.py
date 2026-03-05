import cadquery as cq

# Parameters (adjust as needed)
t = 2.0          # sheet thickness (unused in simplified profile)
width = 10.0     # clip width (extrusion depth)
H1 = 80.0        # height of back leaf
H2 = 60.0        # height where inner leaf ends before bulge
R = 10.0         # bend radius for the top loop
bulge_r = 5.0    # radius of the bottom bulge

result = (
    cq.Workplane("XZ")
      .moveTo(0, 0)
      .lineTo(0, H1)
      .threePointArc((R, H1 + R), (2 * R, H1))
      .lineTo(2 * R, H2)
      .threePointArc((2 * R + bulge_r, H2 - bulge_r), (2 * R, H2 - 2 * bulge_r))
      .lineTo(0, H2 - 2 * bulge_r)
      .close()
      .extrude(width)
)
