import cadquery as cq

base_cylinder = cq.Workplane("XY").circle(20).extrude(100)

flange = (
    cq.Workplane("XY")
    .circle(25)
    .extrude(10)
    .faces(">Z")
    .workplane()
    .circle(20)
    .cutThruAll()
)

connector = (
    cq.Workplane("XY")
    .rect(40, 20)
    .extrude(10)
    .faces(">Z")
    .workplane()
    .circle(5)
    .cutBlind(-10)
)

flange_with_connector = flange.union(
    connector.translate((0, 0, 10))
)

flange_with_connector_and_hole = flange_with_connector.union(
    cq.Workplane("XY")
    .circle(20)
    .extrude(5)
    .translate((0, 0, -5))
)

full_model = base_cylinder.union(
    flange_with_connector_and_hole.translate((0, 0, 100))
)
final_model = full_model.union(
    flange_with_connector_and_hole.mirror("XY").translate((0, 0, -5))
)

result = final_model