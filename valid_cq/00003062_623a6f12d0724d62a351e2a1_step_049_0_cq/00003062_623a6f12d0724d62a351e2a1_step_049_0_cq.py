import cadquery as cq

# Parametric dimensions
width = 50.0       # Width of the rectangular section
length = 60.0      # Length from center of circle to end of rectangle
thickness = 15.0   # Thickness of the top and bottom plates
gap = 10.0         # Gap between the top and bottom plates
radius = width / 2 # Radius of the rounded end
shaft_radius = 18.0 # Radius of the connecting shaft/cylinder

# Create the basic profile shape (a rectangle with a semi-circle on one end)
# We sketch on the XY plane.
# Center of the circle part is at (0,0)
def create_plate_profile():
    return (
        cq.Workplane("XY")
        .moveTo(0, -radius)
        .lineTo(length, -radius)
        .lineTo(length, radius)
        .lineTo(0, radius)
        .threePointArc((-radius, 0), (0, -radius))
        .close()
    )

# 1. Create the bottom plate
bottom_plate = (
    create_plate_profile()
    .extrude(thickness)
)

# 2. Create the connecting cylinder (shaft) in the middle
# It starts on top of the bottom plate
mid_cylinder = (
    cq.Workplane("XY")
    .workplane(offset=thickness)
    .circle(shaft_radius)
    .extrude(gap)
)

# 3. Create the top plate
# It starts on top of the mid cylinder
top_plate = (
    create_plate_profile()
    .workplane(offset=thickness + gap)
    .extrude(thickness)
)

# Combine all parts into a single result
result = bottom_plate.union(mid_cylinder).union(top_plate)