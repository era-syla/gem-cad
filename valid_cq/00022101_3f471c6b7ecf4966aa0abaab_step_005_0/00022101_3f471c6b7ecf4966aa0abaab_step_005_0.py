import cadquery as cq

# Parameters for the cylindrical rod
length = 100.0   # Total length of the rod
diameter = 2.0   # Diameter of the circular cross-section

# Create the solid geometry
# Start on the XY plane, draw a circle, and extrude it to create a cylinder
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)