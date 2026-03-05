import cadquery as cq

# Create a flat mounting plate with a central hole and various features
# Base dimensions: long rectangular plate
length = 200
width = 50
thickness = 3

# Create the main base plate
result = (
    cq.Workplane("XY")
    .sketch()
    .rect(length, width)
    .finalize()
    .extrude(thickness)
)

# Create the main plate shape with chamfered corners using vertices
result = (
    cq.Workplane("XY")
    .moveTo(-100, -22)
    .lineTo(-95, -25)
    .lineTo(85, -25)
    .lineTo(100, -15)
    .lineTo(100, 15)
    .lineTo(85, 25)
    .lineTo(-85, 25)
    .lineTo(-100, 15)
    .close()
    .extrude(thickness)
)

# Add central circular hole
result = (
    result
    .faces(">Z")
    .workplane()
    .moveTo(20, 0)
    .circle(18)
    .cutThruAll()
)

# Add mounting holes along the plate
hole_positions = [
    (-80, 18), (-80, -18),
    (80, 18), (80, -18),
    (0, 20), (0, -20),
    (-40, 20), (40, 20),
    (-40, -20), (40, -20),
]

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .circle(2.5)
    .cutThruAll()
)

# Add small boss/cylinder features on the left side
result = (
    result
    .faces(">Z")
    .workplane()
    .moveTo(-85, 0)
    .circle(5)
    .extrude(3)
)

result = (
    result
    .faces(">Z")
    .workplane()
    .moveTo(-85, 0)
    .circle(2.5)
    .cutThruAll()
)

# Add a raised lip/step on the left portion
result = (
    result
    .faces(">Z")
    .workplane()
    .moveTo(-60, 0)
    .rect(70, 44)
    .extrude(1.5)
)

# Trim the raised portion to fit within the main plate shape
# by cutting away what extends beyond
result = (
    result
    .faces(">Z")
    .workplane()
    .moveTo(-60, 0)
    .rect(70, 44)
    .cutThruAll()
)

# Restart with a cleaner approach
result = (
    cq.Workplane("XY")
    .moveTo(-100, -20)
    .lineTo(-88, -25)
    .lineTo(88, -25)
    .lineTo(100, -12)
    .lineTo(100, 12)
    .lineTo(88, 25)
    .lineTo(-88, 25)
    .lineTo(-100, 12)
    .close()
    .extrude(thickness)
)

# Central large hole
result = (
    result
    .faces(">Z")
    .workplane()
    .moveTo(15, 0)
    .circle(17)
    .cutThruAll()
)

# Small mounting holes
for pos in [(-75, 20), (-75, -20), (75, 20), (75, -20),
            (-45, 20), (-45, -20), (45, 20), (45, -20),
            (0, 22), (0, -22)]:
    result = (
        result
        .faces(">Z")
        .workplane()
        .moveTo(pos[0], pos[1])
        .circle(2)
        .cutThruAll()
    )

# Add small cylindrical boss
result = (
    result
    .faces(">Z")
    .workplane()
    .moveTo(-88, 0)
    .circle(4.5)
    .extrude(4)
)

result = (
    result
    .faces(">Z")
    .workplane()
    .moveTo(-88, 0)
    .circle(2)
    .cutThruAll()
)

# Add slight raised step on left side top face
left_step = (
    cq.Workplane("XY")
    .workplane(offset=thickness)
    .moveTo(-70, 0)
    .rect(50, 40)
    .extrude(1.5)
)

result = result.union(left_step)