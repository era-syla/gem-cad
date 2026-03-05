import cadquery as cq

thickness = 5.0
# Define the 2D profile of the plate
profile = [
    (15, 15),
    (60, 15),
    (60, 25),
    (50, 25),
    (50, 50),
    (0, 50),
]

# Extrude the profile to create the solid
result = cq.Workplane("XY").polyline(profile).close().extrude(thickness)

# Define hole positions
big_holes = [(20, 45), (20, 35), (20, 25)]
small_holes = [(5, 7.5), (15, 7.5), (25, 7.5), (35, 7.5), (45, 7.5), (55, 7.5)]

# Drill holes through the thickness
result = (
    result
    .faces(">Z").workplane()
    .pushPoints(big_holes).hole(10)
    .pushPoints(small_holes).hole(5)
)