import cadquery as cq

# Parameters for the torus
major_radius = 40
minor_radius = 5

# Create a circular profile in the XZ plane offset along X by the major radius, then revolve around Z
result = (
    cq.Workplane("XZ")
      .circle(minor_radius)
      .translate((major_radius, 0, 0))
      .revolve(360, axisStart=(0, 0, 0), axisEnd=(0, 0, 1))
)