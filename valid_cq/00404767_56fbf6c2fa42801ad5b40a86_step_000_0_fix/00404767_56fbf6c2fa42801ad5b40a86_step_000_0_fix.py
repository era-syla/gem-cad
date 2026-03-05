import cadquery as cq

# Define the 2D profile of the turned part as (radius, height) points
profile = [
    (0, 0),      # tip center
    (2, 30),     # end of conical tip
    (10, 40),    # start of neck
    (12, 60),    # end of neck
    (16, 80),    # start of top cylinder
    (16, 100),   # top of cylinder
    (0, 100),    # back to axis
]

# Build and revolve the profile to create the solid
result = (
    cq.Workplane("XY")
      .polyline(profile)
      .close()
      .revolve(360)
)