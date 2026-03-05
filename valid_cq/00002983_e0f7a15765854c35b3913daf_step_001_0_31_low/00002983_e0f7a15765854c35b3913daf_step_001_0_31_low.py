import cadquery as cq

# Parameters
length = 100.0
width = 30.0
height = 20.0
fillet_radius = 10.0

# Create the base block
base = cq.Workplane("XY").box(length, width, height)

# Apply fillets to the two opposite edges on the top face
result = base.edges(">Z").edges("<X or >X").fillet(fillet_radius)