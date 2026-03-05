import cadquery as cq

# Parameters
flange_dia = 25.0
flange_thickness = 2.0
pulley_dia = 19.5
pulley_length = 14.0
bore_dia = 5.0
num_teeth = 20
groove_dia = 2.0

# Create the main cylindrical body of the pulley
result = (
    cq.Workplane("XY")
    .circle(pulley_dia / 2)
    .extrude(pulley_length)
)

# Cut the teeth grooves into the pulley body
result = (
    result.faces(">Z").workplane()
    .polarArray(pulley_dia / 2, 0, 360, num_teeth)
    .circle(groove_dia / 2)
    .cutThruAll()
)

# Add the bottom flange
result = (
    result.faces("<Z").workplane()
    .circle(flange_dia / 2)
    .extrude(flange_thickness)
)

# Add the top flange
result = (
    result.faces(">Z").workplane()
    .circle(flange_dia / 2)
    .extrude(flange_thickness)
)

# Cut the central bore hole through the entire assembly
result = (
    result.faces(">Z").workplane()
    .circle(bore_dia / 2)
    .cutThruAll()
)