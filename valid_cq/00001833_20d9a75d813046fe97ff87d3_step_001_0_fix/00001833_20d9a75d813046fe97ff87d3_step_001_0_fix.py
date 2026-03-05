import cadquery as cq

# Parameters
width = 40.0
peak_height = 55.0
valley_height = 45.0
thickness = 20.0
ring_outer_r = 8.0
ring_inner_r = 4.0
ring_thickness = 3.0

# Create the wavy panel by defining its side profile in the XZ plane and extruding along Y
profile_points = [
    (0, 0),
    (0, peak_height),
    (width/2, valley_height),
    (width, peak_height),
    (width, 0)
]
panel = (
    cq.Workplane("XZ")
      .polyline(profile_points)
      .close()
      .extrude(thickness)
)

# Create the ring on the side: build outer cylinder and subtract inner cylinder
ring_outer = (
    cq.Workplane("YZ")
      .center(thickness/2, peak_height/2)
      .circle(ring_outer_r)
      .extrude(-ring_thickness)
)
ring_inner = (
    cq.Workplane("YZ")
      .center(thickness/2, peak_height/2)
      .circle(ring_inner_r)
      .extrude(-ring_thickness)
)
ring = ring_outer.cut(ring_inner)

# Combine the panel and the ring
result = panel.union(ring)