import cadquery as cq

text = "Ed Schenamisk"
text_depth = 1
plate_length = 60
plate_width = 20
plate_height = 2
border_size = 2

plate = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_height)
)

border = (
    plate.faces(">Z")
    .workplane()
    .rect(plate_length - border_size, plate_width - border_size)
    .cutBlind(-plate_height)
)

text_object = (
    border.faces(">Z")
    .workplane()
    .text(text, 8, text_depth, cut=True)
)

result = text_object
