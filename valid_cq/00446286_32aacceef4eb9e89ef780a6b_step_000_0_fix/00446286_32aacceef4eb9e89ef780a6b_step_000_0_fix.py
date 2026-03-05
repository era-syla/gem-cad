import cadquery as cq

# Parameters
plate_width = 40
plate_height = 40
plate_thickness = 2
gap = 2
step_width = 15
step_height = 10
rod_width = 3
rod_depth = plate_thickness
rod_height = 50
rod_spacing = 10

# Back plate
back_plate = cq.Workplane("XZ").box(plate_width, plate_thickness, plate_height)
back_plate = back_plate.translate((0, - (plate_thickness/2 + gap/2), 0))

# Front plate: main body
main_body = cq.Workplane("XZ").box(plate_width, plate_thickness, plate_height - step_height)
# Front plate: step body
step_body = cq.Workplane("XZ").box(step_width, plate_thickness, plate_height)
step_body = step_body.translate(((plate_width - step_width)/2, 0, 0))
front_plate = main_body.union(step_body)
front_plate = front_plate.translate((0, (plate_thickness/2 + gap/2), 0))

# Pins (rods) on back plate
y_back = - (plate_thickness/2 + gap/2)
z0 = plate_height/2
x1 = -rod_spacing/2
x2 = rod_spacing/2
rod1 = cq.Workplane("XY").transformed(offset=(x1, y_back, z0)).rect(rod_width, rod_depth).extrude(rod_height)
rod2 = cq.Workplane("XY").transformed(offset=(x2, y_back, z0)).rect(rod_width, rod_depth).extrude(rod_height)

# Combine all parts
result = back_plate.union(front_plate).union(rod1).union(rod2)