import cadquery as cq

# Parameters
length = 100.0
width = 40.0
thickness = 5.0

cutout_width = 10.0
cutout_depth = 5.0
cutout_spacing = 30.0

hole_dia = 6.0
hole_spacing = 15.0

# Base plate
result = cq.Workplane("XY").box(length, width, thickness)

# Side cutouts
result = (
    result
    .faces(">Z").workplane()
    .pushPoints([
        (cutout_spacing/2, width/2), 
        (-cutout_spacing/2, width/2),
        (cutout_spacing/2, -width/2), 
        (-cutout_spacing/2, -width/2)
    ])
    .rect(cutout_width, cutout_depth*2)
    .cutThruAll()
)

# End cutouts
result = (
    result
    .faces(">Z").workplane()
    .pushPoints([
        (length/2, width/2), 
        (-length/2, width/2),
        (length/2, -width/2), 
        (-length/2, -width/2)
    ])
    .rect(cutout_width, cutout_depth*2)
    .cutThruAll()
)

# Holes
result = (
    result
    .faces(">Z").workplane()
    .pushPoints([
        (hole_spacing/2, 0),
        (-hole_spacing/2, 0)
    ])
    .hole(hole_dia)
)