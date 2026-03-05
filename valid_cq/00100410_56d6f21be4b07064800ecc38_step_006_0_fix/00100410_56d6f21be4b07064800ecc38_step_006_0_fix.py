import cadquery as cq

# Create the Perrinn logo: an outer ring with three spoke holes and a center hole
logo = (
    cq.Workplane("XY")
    .circle(20)       # outer circle radius 20
    .circle(18)       # inner circle radius 18, so ring thickness = 2
    .extrude(1)       # ring thickness = 1
    .faces(">Z")
    .workplane()
    .pushPoints([(0, 10), (8.660254, -5), (-8.660254, -5)])  # 3 spoke hole centers at radius 10, 120° apart
    .circle(4)        # spoke hole radius = 4
    .cutThruAll()     # cut through the ring
    .faces(">Z")
    .workplane()
    .circle(5)        # center hole radius = 5
    .cutThruAll()
)

# Create the text "PERRINN" as raised letters
text = (
    cq.Workplane("XY")
    .text("PERRINN", 5, 1)  # font height = 5, text depth (extrusion) = 1
    .translate((-40, 0, 0)) # move text to the left of the logo
)

# Combine logo and text into the final result
result = logo.union(text)