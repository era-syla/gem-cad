import cadquery as cq

# Parametric dimensions for the rod
length = 100.0   # Total length of the rod
diameter = 2.0   # Diameter of the rod

# Create the solid geometry
# Generates a vertical cylinder by sketching a circle on the XY plane and extruding it
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)