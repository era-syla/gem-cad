import cadquery as cq

# Parameters
height = 80.0
core_diameter = 4.0
rib_thickness = 0.5
rib_width = 2.0
rib_count = 4

# Core cylinder
core = cq.Workplane("XY").circle(core_diameter/2).extrude(height)

# Single rib profile, extruded along Z, positioned on X+
rib = (
    cq.Workplane("XY")
    .rect(rib_thickness, rib_width)
    .extrude(height)
    .translate((core_diameter/2 + rib_thickness/2, 0, 0))
)

# Assemble ribs around the core
result = core
for i in range(rib_count):
    angle = 360.0 / rib_count * i
    result = result.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))