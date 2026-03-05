import cadquery as cq

# Dimensions
big_radius = 15
small_radius = 7
thickness = 3
length = 60

# Create the big end
big_end = (
    cq.Workplane("XY")
    .circle(big_radius)
    .extrude(thickness)
)

# Create the small end
small_end = (
    cq.Workplane("XY")
    .center(length, 0)
    .circle(small_radius)
    .extrude(thickness)
)

# Create the connecting arm
arm_profile = (
    cq.Workplane("XY")
    .moveTo(big_radius, thickness / 2)
    .lineTo(length - small_radius, thickness / 2)
    .lineTo(length - small_radius, -thickness / 2)
    .lineTo(big_radius, -thickness / 2)
    .close()
)
arm = arm_profile.extrude(thickness)

# Combine all parts
result = big_end.union(small_end).union(arm)