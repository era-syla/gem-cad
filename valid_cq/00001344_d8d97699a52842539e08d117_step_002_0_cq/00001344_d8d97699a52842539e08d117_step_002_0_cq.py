import cadquery as cq

# Parametric dimensions
length = 50.0   # Total length of the pin
diameter = 5.0  # Diameter of the pin
chamfer_size = 0.5 # Size of the chamfer on the ends

# Create the main cylinder
pin = cq.Workplane("XY").circle(diameter / 2).extrude(length)

# Select the edges at both ends for chamfering
# We select edges that belong to the top and bottom faces (Z-min and Z-max)
result = (
    pin.faces("<Z or >Z")  # Select the bottom and top faces
    .edges()               # Get the edges of those faces
    .chamfer(chamfer_size) # Apply chamfer
)