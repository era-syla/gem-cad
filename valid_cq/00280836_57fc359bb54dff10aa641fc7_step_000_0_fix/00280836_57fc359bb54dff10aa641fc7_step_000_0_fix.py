import cadquery as cq

# Parameters for the model
length = 100
width = 10
height = 5
taper_length = 40

# Create the main block
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .faces(">Y")
    .workplane(centerOption="CenterOfMass")
    .transformed(offset=(taper_length/2, 0, 0))
    .lineTo(taper_length, 0)
    .lineTo(taper_length, height)
    .lineTo(0, height)
    .close()
    .cutBlind(-width/2)
    .faces("<Y")
    .workplane(centerOption="CenterOfMass")
    .transformed(offset=(-taper_length/2, 0, 0))
    .lineTo(-taper_length, 0)
    .lineTo(-taper_length, height)
    .lineTo(0, height)
    .close()
    .cutBlind(-width/2)
)