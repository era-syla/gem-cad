import cadquery as cq

# Parametric dimensions based on the image estimation
pipe_od = 50.0            # Outer Diameter
wall_thickness = 2.5      # Thickness of the pipe wall
bend_radius = 50.0        # Radius of the 90-degree bend
short_leg_length = 25.0   # Length of the shorter vertical section
long_leg_length = 140.0   # Length of the longer horizontal section

# 1. Define the sweep path
# We create a wire on the XZ plane. 
# The path consists of:
# - A vertical line moving up (along Z)
# - A 90-degree tangent arc (bending towards X)
# - A horizontal line extending along X
path = (
    cq.Workplane("XZ")
    .moveTo(0, -short_leg_length)         # Start point
    .lineTo(0, 0)                         # Vertical segment to the bend start
    .tangentArcPoint((bend_radius, bend_radius)) # 90-degree bend
    .lineTo(bend_radius + long_leg_length, bend_radius) # Long straight segment
)

# 2. Create the profile and sweep
# The profile is defined on the XY plane (perpendicular to the start of the path).
# We offset the workplane to the Z-height of the path start point.
# We draw two concentric circles to create the hollow pipe profile.
result = (
    cq.Workplane("XY")
    .workplane(offset=-short_leg_length)
    .circle(pipe_od / 2.0)
    .circle((pipe_od / 2.0) - wall_thickness)
    .sweep(path)
)