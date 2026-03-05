import cadquery as cq

# Parametric dimensions
outer_diameter = 80.0
inner_diameter = 48.0
thickness = 6.0
notch_radius = 4.5
notch_count = 6

# Create the base ring
# Draw outer and inner circles on XY plane and extrude
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
)

# Create the notches
# Select the top face, create a workplane, and pattern the cutting circles
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(
        radius=outer_diameter / 2.0, 
        startAngle=0, 
        angle=360, 
        count=notch_count
    )
    .circle(notch_radius)
    .cutThruAll()
)