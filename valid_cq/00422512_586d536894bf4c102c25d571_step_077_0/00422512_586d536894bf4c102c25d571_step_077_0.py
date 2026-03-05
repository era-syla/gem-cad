import cadquery as cq

# Parametric dimensions for the dowel pin
diameter = 10.0      # Outer diameter of the pin
length = 30.0        # Total length of the pin
chamfer_size = 1.0   # Size of the chamfer at the ends

# Generate the 3D model
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
    .faces("<Z or >Z")   # Select both the bottom and top faces
    .chamfer(chamfer_size)
)