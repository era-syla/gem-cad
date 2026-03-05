import cadquery as cq

# Dimensions
outer_radius = 10
inner_radius = 4
length = 60
hole_radius = 2

# Create the main cylinder (tube)
result = (
    cq.Workplane("YZ")
    .circle(outer_radius)
    .extrude(length)
)

# Create the axial hole through the center
result = (
    result
    .faces(">X")
    .workplane()
    .circle(inner_radius)
    .cutThruAll()
)

# Add two small radial holes on the side (visible in the image)
# First hole - on one side along the length
result = (
    result
    .workplane(offset=0)
    .transformed(offset=cq.Vector(0, 0, 0))
)

# Create radial holes perpendicular to the main axis
# Position them at about 1/4 and 3/4 along the length
result = (
    cq.Workplane("YZ")
    .circle(outer_radius)
    .extrude(length)
)

# Axial through hole
result = (
    result
    .faces(">X")
    .workplane()
    .circle(inner_radius)
    .cutThruAll()
)

# Radial holes - cut through the cylinder perpendicular to main axis
# First radial hole near one end
result = (
    result
    .workplane(offset=length * 0.25)
    .center(0, 0)
    .circle(hole_radius)
    .cutThruAll()
)

# Second radial hole near other end
result = (
    result
    .faces(">X")
    .workplane(offset=-length * 0.25)
    .circle(hole_radius)
    .cutThruAll()
)