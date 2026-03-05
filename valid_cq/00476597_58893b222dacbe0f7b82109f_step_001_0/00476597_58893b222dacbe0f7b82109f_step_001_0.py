import cadquery as cq

# Geometric parameters
length = 60.0       # Total length of the pin
diameter = 16.0     # External diameter
fillet_radius = 2.5 # Radius for the rounded ends

# Create the base cylinder
# 1. Establish a workplane (XY)
# 2. Draw the base circle
# 3. Extrude to the specified length
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)

# Apply fillets to the edges at both ends
# Selecting all edges is effective here as the cylinder primarily consists of the top and bottom loops
result = result.edges().fillet(fillet_radius)