import cadquery as cq

# Parameters defining the U-shape geometry
tube_diameter = 8.0
width_center_to_center = 60.0  # Distance between leg centers
leg_length = 90.0

# Derived dimensions
tube_radius = tube_diameter / 2.0
bend_radius = width_center_to_center / 2.0

# 1. Define the sweep path
# The path is drawn on the XY plane, centered around the Y-axis
path = (
    cq.Workplane("XY")
    .moveTo(-bend_radius, leg_length)         # Start at the top of the left leg
    .lineTo(-bend_radius, 0)                  # Line down to the start of the bend
    .threePointArc((0, -bend_radius), (bend_radius, 0)) # 180-degree semi-circular bend
    .lineTo(bend_radius, leg_length)          # Line up the right leg
)

# 2. Create the cross-section profile and sweep
# The profile needs to be on a plane perpendicular to the start of the path.
# The path starts at (-bend_radius, leg_length, 0) and moves in the -Y direction.
# We use the XZ plane (which has a -Y normal in standard orientation) and offset it.
result = (
    cq.Workplane("XZ")
    .workplane(offset=-leg_length)            # Move plane origin to Y = leg_length
    .moveTo(-bend_radius, 0)                  # Center profile at start of path
    .circle(tube_radius)                      # Create circular profile
    .sweep(path)                              # Sweep along the defined path
)