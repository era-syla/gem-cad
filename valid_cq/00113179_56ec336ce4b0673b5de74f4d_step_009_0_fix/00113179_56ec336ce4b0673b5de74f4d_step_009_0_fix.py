import cadquery as cq
import math

# Parameters
r = 8           # radius of each lobe
lobe_len = 60   # length of the lobed cylinder section
center_dist = 15  # distance from center to each lobe center
block_thickness = 20  # thickness of the octagonal block
octagon_diameter = 2 * r + 20  # diameter of the octagon face
nut_radius = 6
nut_height = 12

# Build the triple-lobed cylinder section
lobes = cq.Workplane("YZ")
for angle in (0, 120, 240):
    y = center_dist * math.cos(math.radians(angle))
    z = center_dist * math.sin(math.radians(angle))
    lobes = lobes.union(
        cq.Workplane("YZ")
          .transformed(offset=(0, y, z))
          .circle(r)
          .extrude(lobe_len)
    )

# Build the octagonal block at the front of the lobes
block = (
    cq.Workplane("YZ")
      .transformed(offset=(lobe_len, 0, 0))
      .polygon(8, octagon_diameter)
      .extrude(-block_thickness)
)

# Union the lobes and the block
base = lobes.union(block)

# Build the hex nut on top of the octagonal block
nut = (
    cq.Workplane("XY")
      .transformed(offset=(lobe_len, 0, octagon_diameter/2))
      .polygon(6, 2 * nut_radius)
      .extrude(nut_height)
)

# Final result
result = base.union(nut)