import cadquery as cq

# Parameters
rail_length = 200
rail_width = 30
rail_height = 10
end_thickness = 10
end_height = 30
rod_dia = 8
rod_offset = 10
car_length = 50
car_width = 50
car_height = 20
hole_dia = 5
hole_positions = [-15, 0, 15]

# Base rail
rail = cq.Workplane("XY").box(rail_length, rail_width, rail_height)

# End caps
end_cap = cq.Workplane("XY").box(end_thickness, rail_width, end_height)
end1 = end_cap.translate(( rail_length/2 - end_thickness/2, 0, (end_height - rail_height)/2 ))
end2 = end_cap.translate((-rail_length/2 + end_thickness/2, 0, (end_height - rail_height)/2 ))

# Guide rods
rod_length = rail_length + 20
rod1 = cq.Workplane("XY").circle(rod_dia/2).extrude(rod_length).translate((0, rod_offset, rail_height/2))
rod2 = cq.Workplane("XY").circle(rod_dia/2).extrude(rod_length).translate((0, -rod_offset, rail_height/2))

# Carriage block
carriage = cq.Workplane("XY").box(car_length, car_width, car_height)

# Top mounting hole pattern
for x in hole_positions:
    for y in hole_positions:
        carriage = carriage.faces(">Z").workplane().center(x, y).hole(hole_dia)

# Side through-holes for rods
carriage = carriage.faces(">Y").workplane(centerOption="CenterOfBoundBox").hole(rod_dia + 0.2)
carriage = carriage.faces("<Y").workplane(centerOption="CenterOfBoundBox").hole(rod_dia + 0.2)

# Position carriage above rail
carriage = carriage.translate((0, 0, rail_height + car_height/2))

# Assemble all parts
result = rail.union(end1).union(end2).union(rod1).union(rod2).union(carriage)