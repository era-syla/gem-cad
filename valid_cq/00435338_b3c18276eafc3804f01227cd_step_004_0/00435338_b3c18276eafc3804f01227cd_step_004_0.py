import cadquery as cq

# Dimensions based on the image proportions
outer_diameter = 100.0
inner_diameter = 70.0
thickness = 6.0
bolt_circle_diameter = 85.0
hole_count = 12
hole_diameter = 5.0

# Create the base flange geometry
# Draw outer and inner circles on the XY plane and extrude to create a ring
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
)

# Create the circular pattern of holes
# Select the top face, apply a polar array, and cut the holes through the part
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=bolt_circle_diameter / 2.0, startAngle=0, angle=360, count=hole_count)
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)