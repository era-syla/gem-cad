import cadquery as cq

# Parameters
plate_length = 120
plate_width = 20
plate_thickness = 3
prong_length = 20
prong_width = 5
prong_height = 15

# Offsets for prongs
x_off = (plate_width - prong_width) / 2
y_off = plate_length / 2 - prong_length / 2

result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    # Engrave text on the top of the plate
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .text("Prusa i3", 10, -0.8)
    # Add prongs on each end
    .faces(">Z")
    .workplane()
    .pushPoints([( x_off,  y_off),
                 (-x_off,  y_off),
                 ( x_off, -y_off),
                 (-x_off, -y_off)])
    .rect(prong_width, prong_length)
    .extrude(prong_height)
)