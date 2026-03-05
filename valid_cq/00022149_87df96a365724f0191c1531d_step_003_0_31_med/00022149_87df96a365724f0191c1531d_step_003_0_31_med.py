import cadquery as cq

# Parameters
r1 = 25.0       # Radius of the main cylinder
h1 = 90.0       # Height of the main cylinder
r2 = 18.0       # Radius of the second stepped cylinder
h2 = 15.0       # Height of the second stepped cylinder
r3 = 8.0        # Radius of the top button
h3 = 2.0        # Height of the top button
r4 = 1.5        # Radius of the center hole
h4 = 2.0        # Depth of the center hole

# Create the 3D model
result = (
    cq.Workplane("XY")
    .circle(r1)
    .extrude(h1)
    .faces(">Z")
    .workplane()
    .circle(r2)
    .extrude(h2)
    .faces(">Z")
    .workplane()
    .circle(r3)
    .extrude(h3)
    .faces(">Z")
    .workplane()
    .circle(r4)
    .cutBlind(-h4)
)