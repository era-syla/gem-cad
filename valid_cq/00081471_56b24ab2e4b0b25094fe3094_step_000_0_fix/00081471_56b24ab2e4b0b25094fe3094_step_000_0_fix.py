import cadquery as cq

# Parameters
thickness = 5
leg_width = 12
horizontal_length = 50
vertical_height = 80
taper_height = 30
top_width = 6
offset = (leg_width - top_width) / 2
hole_dia = 6

# Sketch and extrude the bracket profile
result = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (horizontal_length, 0),
        (horizontal_length, leg_width),
        (leg_width, leg_width),
        (leg_width, leg_width + vertical_height),
        (leg_width - offset, leg_width + vertical_height + taper_height),
        (offset, leg_width + vertical_height + taper_height),
        (0, leg_width)
    ])
    .close()
    .extrude(thickness)
    # Add holes on the top face
    .faces(">Z")
    .workplane()
    .pushPoints([
        (horizontal_length/2, leg_width/2),
        (leg_width/2, leg_width + vertical_height/2),
        (leg_width/2, leg_width + vertical_height + taper_height/3),
        (leg_width/2, leg_width + vertical_height + 2*taper_height/3),
        (leg_width/2, leg_width + vertical_height + taper_height - top_width/2)
    ])
    .hole(hole_dia)
)