import cadquery as cq

# Parameters
inner_width = 20
thickness = 2
height = 30
lip = 1
length = 200

outer_width = inner_width + 2 * thickness

# Build U-channel with outward lips
result = (
    cq.Workplane("XY")
    .polyline([
        (-outer_width/2,  height/2),
        ( outer_width/2,  height/2),
        ( outer_width/2, -height/2),
        ( outer_width/2 - thickness, -height/2),
        ( outer_width/2 - thickness, -height/2 + lip),
        (-outer_width/2 + thickness + lip, -height/2 + lip),
        (-outer_width/2 + thickness, -height/2),
        (-outer_width/2, -height/2)
    ])
    .close()
    .extrude(length)
)