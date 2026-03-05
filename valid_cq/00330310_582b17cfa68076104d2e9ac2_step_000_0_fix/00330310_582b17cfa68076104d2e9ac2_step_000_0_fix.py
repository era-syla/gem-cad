import cadquery as cq

# Create the base 2D profile
profile = (
    cq.Workplane("XY")
    .moveTo(10, 0).lineTo(20, 0)
    .lineTo(30, 20).lineTo(30, 40)
    .lineTo(20, 50).lineTo(10, 50)
    .lineTo(0, 40).lineTo(0, 20)
    .close()
)

# Extrude to create the 3D shape
result = profile.extrude(5)

# Add holes at the specified locations
hole_positions = [(5, 5), (25, 5), (25, 45), (5, 45), (15, 25)]
for pos in hole_positions:
    result = result.faces(">Z").workplane().center(*pos).hole(3)