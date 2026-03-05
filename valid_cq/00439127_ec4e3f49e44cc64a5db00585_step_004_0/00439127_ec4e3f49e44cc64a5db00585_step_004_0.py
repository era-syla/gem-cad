import cadquery as cq

# Parametric dimensions
length = 50.0       # Total length of the pin
diameter = 10.0     # Outer diameter of the pin
chamfer_size = 1.0  # Size of the chamfer at the ends

# Create the cylindrical body
# Start on the XY plane, draw a circle, and extrude it to the specified length
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)

# Apply chamfers to both ends
# Select the faces at the extreme Z coordinates (bottom and top),
# get their edges, and apply the chamfer operation
result = result.faces("<Z or >Z").edges().chamfer(chamfer_size)