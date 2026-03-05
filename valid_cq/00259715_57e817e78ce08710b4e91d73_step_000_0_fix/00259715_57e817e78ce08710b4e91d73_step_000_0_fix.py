import cadquery as cq

# Create the central supporting rod
rod = cq.Workplane("XY").box(10, 10, 100)

# Create a blade
blade_profile = cq.Workplane("XY").moveTo(0, 15).spline(
    [(0, 15), (20, 50), (50, 40), (60, 10)]
).close()

blade = blade_profile.extrude(2)
blade = blade.faces(">Z").shell(1)

# Create an array of blades around a circle
blades = (
    cq.Workplane("XY")
    .polarArray(30, 0, 270, 10)
    .eachpoint(lambda loc: blade.val().moved(loc), True)
)

# Combine the rod and blades
result = rod.union(blades)