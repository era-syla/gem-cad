import cadquery as cq

# Parameters for the rod geometry
length = 150.0  # Length of the rod
diameter = 3.0  # Diameter of the rod

# Create a solid cylindrical rod
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)