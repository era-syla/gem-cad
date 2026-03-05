import cadquery as cq

# Base dimensions
length = 100
width = 50
thickness = 5
base_length = 80
base_thickness = 8

# Create the main fin shape
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(base_length, 0)
    .lineTo(base_length - 20, width)
    .threePointArc((length/2 - 10, width + 20), (0, width))
    .close()
    .extrude(thickness)
)

# Add fillets to edges
result = result.edges("|Z").fillet(2)

# Create the base block
base = (
    cq.Workplane("XY")
    .box(base_length + 20, 10, base_thickness)
    .translate((base_length/2 - 10, -5, base_thickness/2 - thickness/2))
)

# Combine fin and base
result = result.union(base)

# Add holes
result = (
    result.faces(">Z").workplane()
    .pushPoints([(10, -5), (base_length - 10, -5)])
    .hole(3)
)

# Add base cutout
result = (
    result.faces("<Z").workplane()
    .center(base_length/2 - 10, -5)
    .rect(20, 10)
    .extrude(-2, combine="s")
)
