import cadquery as cq

# Parameters
rod_dia = 12
rod_spacing = 40
rod_length = 200
plate_thick = 10
plate_size = 60
slider_w = 50
slider_d = 40
slider_h = 20
clearance = 0.2

# Create two guide rods
rod = cq.Workplane("XY").circle(rod_dia/2).extrude(rod_length)
rod1 = rod.translate(( rod_spacing/2, 0, 0))
rod2 = rod.translate((-rod_spacing/2, 0, 0))
rods = rod1.union(rod2)

# Bottom end plate
bottom_plate = (
    cq.Workplane("XY")
    .rect(plate_size, plate_size)
    .extrude(plate_thick)
    .faces(">Z")
    .workplane()
    .pushPoints([( rod_spacing/2, 0), (-rod_spacing/2, 0)])
    .hole(rod_dia)
)

# Top end plate
top_plate = (
    cq.Workplane("XY")
    .rect(plate_size, plate_size)
    .extrude(plate_thick)
    .faces(">Z")
    .workplane()
    .pushPoints([( rod_spacing/2, 0), (-rod_spacing/2, 0)])
    .hole(rod_dia)
    .translate((0, 0, rod_length - plate_thick))
)

# Slider block
slider = (
    cq.Workplane("XY")
    .rect(slider_w, slider_d)
    .extrude(slider_h)
    .faces(">Z")
    .workplane()
    .pushPoints([( rod_spacing/2, 0), (-rod_spacing/2, 0)])
    .hole(rod_dia + clearance)
    .translate((0, 0, rod_length/2 - slider_h/2))
)

result = rods.union(bottom_plate).union(top_plate).union(slider)