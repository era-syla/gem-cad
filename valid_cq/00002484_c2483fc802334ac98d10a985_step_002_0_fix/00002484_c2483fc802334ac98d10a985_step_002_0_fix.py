import cadquery as cq

# Define the outer profile of the part in the X–Z plane as (radius, height) pairs
profile = [
    (0, 0),    # axis start
    (30, 0),   # base outer
    (30, 10),  # base height
    (25, 10),  # cavity undercut
    (25, 16),  # cavity taper
    (20, 25),  # mid taper
    (12, 35),  # flange taper
    (8, 50),   # shaft radius
    (8, 60)    # shaft top
]

# Revolve the profile around the Z axis to create the solid body
result = (
    cq.Workplane("XZ")
    .polyline(profile)
    .close()
    .revolve(360, (0, 0, 0), (0, 0, 1))
)

# Cut out the inner cavity at the bottom (for bearing clearance)
result = (
    result
    .faces("<Z")
    .workplane()
    .circle(25)
    .cutBlind(-6)
)

# Bore out the shaft inner hole from the top
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(8)
    .cutBlind(-60)
)

# Add the small locating pin on the bottom center
pin = (
    cq.Workplane("XY")
    .workplane(offset=-5)
    .circle(2)
    .extrude(5)
)

result = result.union(pin)