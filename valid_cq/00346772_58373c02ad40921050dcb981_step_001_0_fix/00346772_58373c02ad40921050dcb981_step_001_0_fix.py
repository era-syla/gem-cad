import cadquery as cq

# Parameters
length = 100
web_width = 15
thickness = 10
end_diameter = 20
hole_diameter = 10
fillet_radius = 3
half_length = length/2

# Base rectangular web
rect = cq.Workplane("XY")\
    .rect(length, web_width)\
    .extrude(thickness)

# End bosses
cyl_left = cq.Workplane("XY")\
    .center(-half_length, 0)\
    .circle(end_diameter/2)\
    .extrude(thickness)

cyl_right = cq.Workplane("XY")\
    .center(half_length, 0)\
    .circle(end_diameter/2)\
    .extrude(thickness)

# Fuse everything
result = rect.union(cyl_left).union(cyl_right)

# Fillet all outer edges
result = result.edges().fillet(fillet_radius)

# Drill through holes in the bosses
result = (
    result.faces(">Z")
      .workplane()
      .center(-half_length, 0)
      .hole(hole_diameter)
      .center(length, 0)
      .hole(hole_diameter)
)