import cadquery as cq

result = (
    cq.Workplane("XY")
    # Left flange
    .circle(12).extrude(3)
    # Small shaft
    .faces(">Z").workplane().circle(6).extrude(5)
    # First collar (ring)
    .faces(">Z").workplane().circle(15).extrude(2)
    # Middle shaft
    .faces(">Z").workplane().circle(8).extrude(8)
    # Second collar (ring)
    .faces(">Z").workplane().circle(15).extrude(2)
    # Right shaft
    .faces(">Z").workplane().circle(5).extrude(20)
    # Hexagonal through-hole from left face
    .faces("<Z").workplane().polygon(6, 6).cutThruAll()
)