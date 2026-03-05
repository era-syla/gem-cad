import cadquery as cq

# Parametric dimensions
tube_radius = 8.0      # Radius of the cross-section
bend_radius = 30.0     # Radius of the 180-degree bend (centerline)
leg_length = 45.0      # Length of the straight vertical section

# 1. Define the Path
# We draw the path on the XZ plane (Front view).
# The path starts at the bottom of the straight leg, goes up, and arcs 180 degrees.
path = (
    cq.Workplane("XZ")
    .moveTo(bend_radius, -leg_length)                     # Start point (Bottom right)
    .lineTo(bend_radius, 0)                               # Straight vertical line
    .threePointArc((0, bend_radius), (-bend_radius, 0))   # 180-degree arc to the left
)

# 2. Define the Profile
# We need a circular profile perpendicular to the start of the path.
# The path starts at global (bend_radius, 0, -leg_length) facing +Z.
# We create the profile on the XY plane, offset to the start Z-level.
profile = (
    cq.Workplane("XY")
    .workplane(offset=-leg_length)
    .moveTo(bend_radius, 0)
    .circle(tube_radius)
)

# 3. Create the Solid
# Sweep the circular profile along the defined path
result = profile.sweep(path)