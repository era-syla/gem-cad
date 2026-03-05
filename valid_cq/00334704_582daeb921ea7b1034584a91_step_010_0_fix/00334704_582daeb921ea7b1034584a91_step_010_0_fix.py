import cadquery as cq

# Parameters
rail_length = 200
rail_width = 10
rail_height = 10
rail_hole_dia = 5
rail_hole_spacing = 20
num_holes = int(rail_length / rail_hole_spacing)

# Create one rail with through holes
base_rail = (
    cq.Workplane("XY")
    .box(rail_length, rail_width, rail_height)
    .faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .rarray(num_holes, 1, rail_hole_spacing, 1)
    .circle(rail_hole_dia / 2)
    .cutThruAll()
)

# Position two parallel rails
rail1 = base_rail.translate((0, -15, rail_height / 2))
rail2 = base_rail.translate((0,  15, rail_height / 2))

# Carriage body
carriage = (
    cq.Workplane("XY")
    .box(40, 30, 10)
    .faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .rect(40, 30)
    .extrude(10)
)

# Reinforcing ribs on top of carriage
rib = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, 10))
    .rect(40, 5)
    .extrude(10)
)
carriage = carriage.union(rib.translate((0, 12.5, 0)))
carriage = carriage.union(rib.translate((0, -12.5, 0)))

# Triangular side braces
brace_profile = [(0, 0), (5, 0), (0, 5)]
brace = (
    cq.Workplane("YZ")
    .transformed(offset=(20, 0, 10))
    .polyline(brace_profile)
    .close()
    .extrude(30)
)
brace2 = brace.translate((-40, 0, 0))
carriage = carriage.union(brace).union(brace2)

# Position carriage on rails
carriage = carriage.translate((0, 0, rail_height + 5))

# Final assembly
result = rail1.union(rail2).union(carriage)