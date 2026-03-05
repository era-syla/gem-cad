import cadquery as cq

# Parametric dimensions
arch_radius = 50.0  # The radius of the bend (major radius)
tube_radius = 5.0   # The radius of the tube (minor radius)

# Create the sweep path: a semi-circle arch in the XZ plane
# Starts at (-arch_radius, 0), goes through top (0, arch_radius), ends at (arch_radius, 0)
path = (
    cq.Workplane("XZ")
    .moveTo(-arch_radius, 0)
    .threePointArc((0, arch_radius), (arch_radius, 0))
)

# Create the tube profile and sweep it along the path
# The profile is a circle on the XY plane, centered at the start of the path
result = (
    cq.Workplane("XY")
    .center(-arch_radius, 0)
    .circle(tube_radius)
    .sweep(path)
)