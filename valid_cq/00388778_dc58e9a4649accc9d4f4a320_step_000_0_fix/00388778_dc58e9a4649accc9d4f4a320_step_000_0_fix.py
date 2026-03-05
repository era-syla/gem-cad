import cadquery as cq

# Parameters
ring_inner_radius = 10
ring_thickness = 1.5
prong_height = 5
prong_radius = 0.5
prong_tip_radius = 1

# Create the ring band
ring_band = cq.Workplane("XY").circle(ring_inner_radius + ring_thickness).circle(ring_inner_radius).extrude(ring_thickness)

# Create a single prong
prong = (cq.Workplane("XY")
         .workplane(offset=ring_thickness)
         .circle(prong_radius)
         .extrude(prong_height)
         .faces(">Z")
         .workplane()
         .circle(prong_tip_radius)
         .extrude(prong_tip_radius))

# Position the prongs
prongs = prong.rotate((0, 0, 0), (0, 0, 1), 90).union(
    prong.rotate((0, 0, 0), (0, 0, 1), 180)).union(
    prong.rotate((0, 0, 0), (0, 0, 1), 270))

# Combine the ring and prongs
result = ring_band.union(prongs)