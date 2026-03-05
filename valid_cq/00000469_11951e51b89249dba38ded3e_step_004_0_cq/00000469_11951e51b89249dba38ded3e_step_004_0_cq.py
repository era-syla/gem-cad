import cadquery as cq

# Parametric dimensions
major_radius = 50.0  # The radius from the center of the ring to the center of the tube
minor_radius = 5.0   # The radius of the tube itself

# Create the torus
# A torus can be created by revolving a circle around an axis.
# CadQuery creates a solid by sweeping a profile. Here we define the cross-section (a circle)
# and sweep it, or use the direct solid creation method if available.
# The most standard way in basic CAD kernels is a revolution.

# Method 1: Revolve a circle
# Create a workplane, draw a circle offset from the origin, and revolve it.
result = (
    cq.Workplane("XZ")
    .center(major_radius, 0)
    .circle(minor_radius)
    .revolve(360, (-major_radius, 0, 0), (-major_radius, 1, 0))
)

# Alternatively, a more idiomatic 'parametric' way often used in simple scripts:
# result = cq.Workplane("XY").torus(major_radius, minor_radius) # Note: CadQuery's .torus() uses major_radius and minor_radius differently depending on version/kernel, usually major is distance to center of tube.

# Let's stick to the explicit revolve method as it's universally clear:
# 1. Start on XZ plane.
# 2. Move to X = major_radius.
# 3. Draw a circle of radius = minor_radius.
# 4. Revolve around the Z axis (which is the vertical axis relative to the XZ plane origin).

result = (
    cq.Workplane("XZ")
    .moveTo(major_radius, 0)
    .circle(minor_radius)
    .revolve(360, (0, 0, 0), (0, 1, 0))
)