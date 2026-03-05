import cadquery as cq

# Parameters
outer_dia = 20.0
inner_dia = 16.0
length = 40.0
flange_dia = 25.0
flange_thickness = 5.0
ring_depth = 0.5      # depth of grooves
ring_width = 0.8      # width of each groove
ring_spacing = ring_width * 1.5  # distance between start of each groove

# Build the main body (threaded portion) and flange
base = cq.Workplane("XY").cylinder(length, outer_dia / 2.0)
flange = cq.Workplane("XY").workplane(offset=length).cylinder(flange_thickness, flange_dia / 2.0)
result = base.union(flange)

# Subtract groove rings to approximate threads
ring_count = int(length / ring_spacing)
for i in range(ring_count):
    zpos = i * ring_spacing
    ring_cut = (
        cq.Workplane("XY")
        .workplane(offset=zpos)
        .cylinder(ring_width, outer_dia / 2.0 + 1.0)
    )
    result = result.cut(ring_cut)

# Subtract the interior bore
total_height = length + flange_thickness
result = result.cut(cq.Workplane("XY").cylinder(total_height, inner_dia / 2.0))