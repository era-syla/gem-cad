import cadquery as cq

outer_radius = 10
hole_diameter = 8
bar_height = 8
thickness = 5
center_distance = 60

# End lobes as cylinders
cyl1 = cq.Workplane("XY").circle(outer_radius).extrude(thickness)
cyl2 = cq.Workplane("XY").transformed(offset=(center_distance, 0, 0)).circle(outer_radius).extrude(thickness)

# Center bar as a rectangular prism
bar = (
    cq.Workplane("XY")
    .transformed(offset=(center_distance/2, 0, 0))
    .rect(center_distance, bar_height)
    .extrude(thickness)
)

# Combine the three solids
combined = cyl1.union(cyl2).union(bar)

# Drill holes through the lobes
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints([(0, 0), (center_distance, 0)])
    .hole(hole_diameter)
)

# Fillet all vertical edges for smooth transitions
result = combined.edges("|Z").fillet(1.5)