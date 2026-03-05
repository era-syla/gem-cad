import cadquery as cq

# -- Parametric Dimensions --
outer_diameter = 200.0       # Outer diameter of the ring
ring_width = 10.0            # Width of the ring material
thickness = 2.0              # Thickness of the plate
num_holes = 72               # Number of holes evenly distributed
hole_diameter = 3.5          # Diameter of the holes

# -- Calculated Values --
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - ring_width
pitch_radius = (outer_radius + inner_radius) / 2.0

# -- Model Generation --

# 1. Create the base washer/ring shape
# We sketch two concentric circles and extrude the area between them
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(thickness)
)

# 2. Cut the pattern of holes
# Select the top face, define a polar array for the bolt circle, and cut holes
result = (
    result
    .faces(">Z")
    .workplane()
    .polarArray(radius=pitch_radius, startAngle=0, angle=360, count=num_holes)
    .hole(hole_diameter)
)