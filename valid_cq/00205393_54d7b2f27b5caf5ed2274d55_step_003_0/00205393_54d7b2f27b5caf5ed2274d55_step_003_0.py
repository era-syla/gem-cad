import cadquery as cq

# Parametric dimensions based on the visual estimate
profile_width = 10.0      # Width of the beam (narrower dimension)
profile_height = 20.0     # Height of the beam (taller dimension)
long_arm_length = 150.0   # Length of the long horizontal beam
short_arm_length = 80.0   # Length of the short beam

# Create the Short Beam (aligned along Y-axis)
# This beam is modeled as the "through" member at the corner.
# Positioned such that its side face lies on the X=0 plane.
# Geometry extends: X from -profile_width to 0, Y from 0 to short_arm_length.
short_beam = (
    cq.Workplane("XY")
    .box(profile_width, short_arm_length, profile_height)
    .translate((-profile_width / 2, short_arm_length / 2, profile_height / 2))
)

# Create the Long Beam (aligned along X-axis)
# This beam butts against the side face of the short beam.
# Geometry extends: X from 0 to long_arm_length, Y from 0 to profile_width.
long_beam = (
    cq.Workplane("XY")
    .box(long_arm_length, profile_width, profile_height)
    .translate((long_arm_length / 2, profile_width / 2, profile_height / 2))
)

# Combine the two beams into a single solid object
result = short_beam.union(long_beam)