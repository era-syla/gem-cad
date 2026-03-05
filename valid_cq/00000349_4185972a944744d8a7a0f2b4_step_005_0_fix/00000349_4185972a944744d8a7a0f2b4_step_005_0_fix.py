import cadquery as cq

# Parameters
length_rect = 50
width = 60
radius = width / 2.0
thickness = 12
D1 = 50   # Large recess diameter
D2 = 30   # Small recess diameter
D3 = 8    # Central through‐hole diameter
H1 = 6    # Large recess depth
H2 = 2    # Small recess depth
mount_hole_d = 4
mount_offset = 5

result = (
    cq.Workplane("XY")
      # Profile: semicircle on left, rectangle to the right
      .moveTo(0, radius)
      .threePointArc((-radius, 0), (0, -radius))
      .lineTo(length_rect, -radius)
      .lineTo(length_rect, radius)
      .close()
      # Extrude to thickness
      .extrude(thickness)
      # Switch to top face for pockets and holes
      .faces(">Z").workplane()
      # Counter‐bored pocket: large then small
      .circle(D1/2).cutBlind(H1)
      .circle(D2/2).cutBlind(H2)
      # Central through‐hole
      .hole(D3)
      # Mounting holes (two on rectangle, one on semicircle)
      .pushPoints([
          (length_rect - mount_offset,  radius - mount_offset),
          (length_rect - mount_offset, -radius + mount_offset),
          (0,                       radius - mount_offset),
      ])
      .hole(mount_hole_d)
)

# 'result' holds the final solid
