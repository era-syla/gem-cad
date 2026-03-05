import cadquery as cq

# Base disk
base = cq.Workplane("XY").circle(30).circle(10).extrude(5)

# Add features
features = (
    cq.Workplane("XY")
    .rect(10, 20).extrude(5)  # Main features
    .faces(">Z").workplane()
    .center(15, 0).circle(3).extrude(5)  # Side features
    .center(-30, 0).circle(3).extrude(5)
    .center(15, 15).circle(3).extrude(5)
)

result = base.union(features)