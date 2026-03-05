import cadquery as cq

# Parameters
margin = 10
radius = 10
d_small = 5
d_large = 6
depth = 20
length = 4 * 2 * radius + 2 * margin
height = margin + radius

# Create the main block
result = cq.Workplane("XZ").rect(length, height).extrude(depth)

# Positions of semicylinders along X
centers = [ -length/2 + margin + radius + i * 2 * radius for i in range(4) ]

# Add half-cylinders on top
for x in centers:
    halfcyl = (
        cq.Workplane("XZ", origin=(x, 0, height))
        .moveTo(-radius, 0)
        .threePointArc((0, radius), (radius, 0))
        .lineTo(-radius, 0)
        .close()
        .extrude(depth)
    )
    result = result.union(halfcyl)

# Heights for holes on front face
z_small = height - radius / 2
z_large = radius

# Small holes under each semicylinder on front face
result = (
    result
    .faces("<Y")
    .workplane()
    .pushPoints([ (x, z_small) for x in centers ])
    .hole(d_small)
)

# Large mounting holes at ends on front face
result = (
    result
    .faces("<Y")
    .workplane()
    .pushPoints([(-length/2 + margin, z_large), (length/2 - margin, z_large)])
    .hole(d_large)
)

# Side holes on left face
result = (
    result
    .faces("<X")
    .workplane()
    .pushPoints([(0, z_small), (0, z_large)])
    .hole(d_small)
)