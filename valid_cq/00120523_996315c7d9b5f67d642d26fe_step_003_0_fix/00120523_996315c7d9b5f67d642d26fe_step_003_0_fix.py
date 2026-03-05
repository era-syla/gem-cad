import cadquery as cq

# Base
base = cq.Workplane("XY").circle(30).extrude(2)

# Pillar
pillar = (cq.Workplane("XY")
          .workplane(offset=2)
          .rect(2, 20)
          .extrude(60))

# Upper Arc
upper_arc = (cq.Workplane("XZ")
             .workplane(offset=50)
             .center(0, 0)
             .circle(10)
             .extrude(5))

# Lower Arc
lower_arc = (cq.Workplane("XZ")
             .workplane(offset=10)
             .center(0, 0)
             .circle(15)
             .extrude(5))

# Combine all parts
result = base.union(pillar).union(upper_arc).union(lower_arc)