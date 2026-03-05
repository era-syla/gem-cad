import cadquery as cq

# Parameters
outer_radius = 10
inner_radius = 4
bar_width = 8
thickness = 5
center_distance = 60

# Create left and right end cylinders
left_cyl = cq.Workplane("XY").cylinder(thickness, outer_radius)
right_cyl = cq.Workplane("XY").cylinder(thickness, outer_radius).translate((center_distance, 0, 0))

# Create the rectangular bar between the cylinders
bar_length = center_distance - 2 * outer_radius
bar = cq.Workplane("XY").rect(bar_length, bar_width).extrude(thickness).translate((center_distance/2, 0, 0))

# Combine solids
result = left_cyl.union(right_cyl).union(bar)

# Add through holes at each end
hole_positions = [(0, 0), (center_distance, 0)]
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .circle(inner_radius)
    .cutThruAll()
)