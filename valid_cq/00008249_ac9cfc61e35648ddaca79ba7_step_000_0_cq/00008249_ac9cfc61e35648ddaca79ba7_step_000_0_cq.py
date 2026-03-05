import cadquery as cq

# --- Parametric Dimensions ---
# These values can be adjusted to change the shape's proportions
rear_diameter = 10.0
front_diameter = 13.0
rear_length = 8.0
transition_length = 5.0
front_straight_length = 6.0
nose_length = 8.0  # Length of the rounded nose section

# --- Calculations ---
rear_radius = rear_diameter / 2.0
front_radius = front_diameter / 2.0

# --- Modeling ---

# We will create the profile and revolve it to ensure perfect symmetry.
# The profile is created on the XZ plane.

# 1. Start at the origin (0,0) - this will be the tip of the nose
# However, it's often easier to build from the back to front or vice versa.
# Let's build from the back face (at x=0) towards the front.

# Points for the profile:
# P0: Center of rear face (0, 0)
# P1: Edge of rear face (0, rear_radius)
# P2: End of rear cylinder (rear_length, rear_radius)
# P3: End of transition/start of front section (rear_length + transition_length, front_radius)
# P4: End of straight front section (rear_length + transition_length + front_straight_length, front_radius)
# P5: Tip of the nose. The nose is an arc.

total_length_before_nose = rear_length + transition_length + front_straight_length
nose_tip_x = total_length_before_nose + nose_length

# Create the profile path
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(0, rear_radius)                        # Rear face radius
    .lineTo(rear_length, rear_radius)              # Rear cylinder
    .lineTo(rear_length + transition_length, front_radius) # Conical transition
    .lineTo(total_length_before_nose, front_radius) # Front straight section
    # Create the ogive/rounded nose. We use a 3-point arc or spline. 
    # A tangent arc is a good approximation for a simple rounded nose.
    # Alternatively, a spline for an ogive shape. Let's use a tangent arc to close at the tip (y=0).
    .radiusArc((nose_tip_x, 0), -front_radius * 2.5) 
    .close() # Close back to (0,0) along the axis
)

# Revolve the profile around the X axis to create the solid
result = profile.revolve(360, (0, 0, 0), (1, 0, 0))

# Export to STEP (optional, for verification)
# cq.exporters.export(result, "projectile.step")