import cadquery as cq

# Parametric dimensions
outer_diameter = 60.0    # Outer diameter of the ring
inner_diameter = 50.0    # Inner diameter of the ring (the hole)
thickness = 8.0          # Height/thickness of the ring
notch_count = 36         # Number of notches around the circumference
notch_radius = 1.5       # Radius of the semicircular notches

# 1. Create the base hollow cylinder (ring)
# Draw outer and inner circles on XY plane and extrude
base_ring = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
)

# 2. Create the cutter objects (cylinders) for the notches
# Use a polar array to position the cutters along the outer circumference
cutters = (
    cq.Workplane("XY")
    .polarArray(
        radius=outer_diameter / 2.0, 
        startAngle=0, 
        angle=360, 
        count=notch_count
    )
    .circle(notch_radius)
    .extrude(thickness)
)

# 3. Cut the notches from the base ring to generate the final geometry
result = base_ring.cut(cutters)