import cadquery as cq

# Create the main plate
plate = cq.Workplane("XY").box(200, 10, 50)

# Create the arm
arm = (
    cq.Workplane("XY")
    .center(0, -5)
    .rect(10, 50)
    .extrude(5)
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .circle(20)
    .extrude(5)
)

# Position the arm on the plate
assembly = plate.union(arm.translate((0, 0, 25)))

# Create perforations
assembly = (
    assembly
    .faces(">Y")
    .workplane(centerOption="CenterOfMass")
    .rarray(30, 10, 5, 2)
    .circle(2)
    .cutThruAll()
)

result = assembly