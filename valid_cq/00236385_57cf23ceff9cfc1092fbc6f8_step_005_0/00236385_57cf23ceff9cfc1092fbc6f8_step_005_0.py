import cadquery as cq

# Parametric dimensions for a long, thin cylindrical rod
# Dimensions estimated based on the visual proportions (approx aspect ratio 50:1)
length = 100.0  # Total length of the rod
diameter = 2.0  # Diameter of the rod

# Create the solid geometry
# Start on the XY plane, draw the cross-section circle, and extrude upwards
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)