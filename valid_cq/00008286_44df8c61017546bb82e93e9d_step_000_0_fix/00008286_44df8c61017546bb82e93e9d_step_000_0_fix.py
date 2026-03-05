import cadquery as cq

rim = cq.Workplane("XY").circle(50).circle(48).extrude(5)
hub = cq.Workplane("XY").circle(8).circle(6).extrude(10)

spoke = cq.Workplane("XZ").circle(0.5).extrude(50)

rim_with_spokes = rim
for i in range(20):
    angle = i * 360 / 20
    spoke_instance = spoke.rotate((0, 0, 0), (0, 1, 0), -45).rotate((0, 0, 0), (0, 0, 1), angle)
    rim_with_spokes = rim_with_spokes.union(spoke_instance)

result = rim_with_spokes.union(hub)