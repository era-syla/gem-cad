import cadquery as cq

# Parametric dimensions
length = 60.0    # Length of the block (X axis)
width = 30.0     # Width/Thickness of the block (Y axis)
height = 40.0    # Height of the block (Z axis)
fillet_radius = 5.0  # Radius of the corner fillets
hole_diameter = 6.0  # Diameter of the central hole

# Create the base block
# We center it to make placing the hole easier (at 0,0)
result = (
    cq.Workplane("XY")
    .box(length, width, height)
)

# Apply fillets to the vertical edges
# We select edges parallel to the Z axis
result = result.edges("|Z").fillet(fillet_radius)

# Create the hole through the center
# Since the block is centered at (0,0,0), we can just drill through the Y axis (front to back)
result = (
    result.faces(">Y")  # Select the front face
    .workplane()
    .hole(hole_diameter)
)

# Alternatively, to ensure it goes all the way through regardless of orientation:
# result = result.faces(">Y").workplane().pushPoints([(0, 0)]).circle(hole_diameter/2).cutThruAll()