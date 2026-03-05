import cadquery as cq

cylinder = cq.Workplane("XY").circle(10).extrude(60)
flange = cq.Workplane("XY").circle(15).extrude(5)
flange = flange.union(flange.mirror("XZ").translate((0, 0, 55)))
connector = cq.Workplane("XY").rect(14, 28).extrude(8)
connector_hole = connector.faces("<Z").workplane().circle(5).cutThruAll()
connector_cut = connector_hole.edges("|Z").fillet(2)
connector = connector_cut.translate((0, 0, -4))
connector = connector.union(connector.mirror("XZ").translate((0, 0, 60)))

result = cylinder.union(flange).union(connector)