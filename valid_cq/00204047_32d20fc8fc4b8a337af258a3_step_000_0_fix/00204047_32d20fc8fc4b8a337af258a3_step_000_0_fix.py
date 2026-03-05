import cadquery as cq

result = (
    cq.Workplane("XY")
    .polyline([(0,0), (75,0), (75,25), (150,25), (150,75), (100,75), (100,125), (0,125)])
    .close()
    .extrude(3)
    .faces(">Z").workplane()
    .rect(75, 25, forConstruction=True)
    .vertices().hole(3)
)