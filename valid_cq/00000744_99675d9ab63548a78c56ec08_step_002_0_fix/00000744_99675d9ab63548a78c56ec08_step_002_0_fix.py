import cadquery as cq

# Linear actuator / hydraulic cylinder assembly

# Main cylinder body
cylinder_radius = 15
cylinder_height = 60

# Build main cylinder
main_body = (
    cq.Workplane("XY")
    .cylinder(cylinder_height, cylinder_radius)
)

# Top cap / end cap
top_cap = (
    cq.Workplane("XY")
    .workplane(offset=cylinder_height/2)
    .cylinder(5, cylinder_radius)
)

# Bottom cap
bottom_cap = (
    cq.Workplane("XY")
    .workplane(offset=-cylinder_height/2)
    .cylinder(5, cylinder_radius)
)

# Piston rod extending from top
rod_radius = 5
rod_height = 50

rod = (
    cq.Workplane("XY")
    .workplane(offset=cylinder_height/2 + 5)
    .cylinder(rod_height, rod_radius)
)

# Hex nut at top of rod
nut_height = 6
nut_width = 12  # across flats

nut = (
    cq.Workplane("XY")
    .workplane(offset=cylinder_height/2 + 5 + rod_height - nut_height/2)
    .polygon(6, nut_width)
    .extrude(nut_height)
)

# Mounting bracket at bottom - two ears with holes
bracket_thickness = 6
bracket_width = 10
bracket_height = 18
ear_separation = 8

# Left ear
left_ear = (
    cq.Workplane("XY")
    .workplane(offset=-cylinder_height/2 - 5 - bracket_height/2)
    .center(-(cylinder_radius + ear_separation/2 + bracket_width/2), 0)
    .box(bracket_width, bracket_thickness, bracket_height)
)

# Right ear
right_ear = (
    cq.Workplane("XY")
    .workplane(offset=-cylinder_height/2 - 5 - bracket_height/2)
    .center((cylinder_radius + ear_separation/2 + bracket_width/2), 0)
    .box(bracket_width, bracket_thickness, bracket_height)
)

# Combine all parts
result = (
    main_body
    .union(top_cap)
    .union(bottom_cap)
    .union(rod)
    .union(nut)
    .union(left_ear)
    .union(right_ear)
)

# Add holes through ears for pin
hole_radius = 3
hole_z = -cylinder_height/2 - 5 - bracket_height/2

result = (
    result
    .faces(">Z[-4]")
    .workplane()
    .center(-(cylinder_radius + ear_separation/2 + bracket_width/2), 0)
    .circle(hole_radius)
    .cutThruAll()
)

result = (
    result
    .faces(">Z[-4]")
    .workplane()
    .center((cylinder_radius + ear_separation/2 + bracket_width/2), 0)
    .circle(hole_radius)
    .cutThruAll()
)

# Add small collar/ring between rod and cylinder top
collar = (
    cq.Workplane("XY")
    .workplane(offset=cylinder_height/2 + 5)
    .circle(rod_radius + 3)
    .circle(rod_radius)
    .extrude(4)
)

result = result.union(collar)