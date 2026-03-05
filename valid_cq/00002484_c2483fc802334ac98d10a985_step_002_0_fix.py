import cadquery as cq

# Build the component from bottom to top (revolve around Z axis)
# This appears to be a multi-tiered rotational part with a base ring,
# stepped body, and top tube/nozzle

result = (
    cq.Workplane("XY")
    # Start with the base ring / flange
    .circle(28)
    .extrude(4)
)

# Add inner raised portion of base
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(22)
    .extrude(3)
)

# Add first step / tier
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(18)
    .extrude(4)
)

# Add second step / tier
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(14)
    .extrude(5)
)

# Add third step / tier (narrower)
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(10)
    .extrude(5)
)

# Add fourth step / tier (even narrower)
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(7)
    .extrude(4)
)

# Add the top tube / nozzle
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(5)
    .extrude(14)
)

# Hollow out the top tube (bore)
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(3)
    .cutBlind(-20)
)

# Add small pin/stem at the bottom
result = (
    result
    .faces("<Z")
    .workplane()
    .circle(1.5)
    .extrude(8)
)

# Add outer groove/channel in the base flange
result = (
    result
    .faces("<Z")
    .workplane()
    .circle(26)
    .circle(23)
    .cutBlind(-2)
)

# Add small collar/lip detail near top tube base
result = (
    result
    .faces(">Z[-3]")
    .workplane()
    .circle(6)
    .extrude(1)
)