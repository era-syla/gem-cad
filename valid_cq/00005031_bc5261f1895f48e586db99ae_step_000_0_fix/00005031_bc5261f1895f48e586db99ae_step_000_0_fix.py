import cadquery as cq

# Parameters
plate_height = 60
plate_width = 12
plate_thickness = 5
hole_offset = 15
hole_diameter = 10
tube_outer_radius = 7
tube_wall_thickness = 2
tube_length = 80

# Derived
hole_y = plate_height/2 - hole_offset
tube_inner_radius = tube_outer_radius - tube_wall_thickness

# Plate
result = cq.Workplane("YZ").rect(plate_height, plate_width).extrude(plate_thickness)

# Mounting holes through plate
result = result.faces(">X").workplane().pushPoints([(0, hole_y), (0, -hole_y)]).hole(hole_diameter)

# Outer tube
outer_tube = cq.Workplane("YZ", origin=(plate_thickness, 0, 0)).circle(tube_outer_radius).extrude(tube_length)
result = result.union(outer_tube)

# Cut inner tube bore
inner_tube = cq.Workplane("YZ", origin=(plate_thickness, 0, 0)).circle(tube_inner_radius).extrude(tube_length + 1)
result = result.cut(inner_tube)

# Triangular rib connecting plate holes to tube center
rib_points = [
    (hole_y,  plate_width/2),
    (-hole_y, plate_width/2),
    (0,        0)
]
rib = cq.Workplane("YZ").polyline(rib_points).close().extrude(plate_thickness)
result = result.union(rib)