import cadquery as cq

# Base platform
base = cq.Workplane("XY").box(100, 100, 20)

# Pole
pole = cq.Workplane("XY").workplane(offset=20).circle(5).extrude(100)

# Arm for solar panel support
arm = cq.Workplane("XZ").workplane(offset=60).move(0, -5).rect(80, 10).extrude(10)

# Solar panel
panel = cq.Workplane("XZ").workplane(offset=70).move(40, -5).rect(90, 60).extrude(5)

# Assemble the components
result = base.union(pole).union(arm).union(panel)