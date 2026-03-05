import cadquery as cq

# Parameters
major_radius = 50  # distance from center to tube center
tube_radius = 5    # radius of the tube

# Build torus by sweeping a circle around the Z axis
result = (
    cq.Workplane("XY")
    .moveTo(major_radius, 0)
    .circle(tube_radius)
    .revolve(360, axisStart=(0, 0, 0), axisEnd=(0, 0, 1))
)