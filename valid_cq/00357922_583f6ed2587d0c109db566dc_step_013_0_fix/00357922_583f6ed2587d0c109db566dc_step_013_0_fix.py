import cadquery as cq

# Define the 2D side profile in the X-Z plane
profile = (
    cq.Workplane("XZ")
    .polyline([
        (0,   0),   # front-bottom
        (90,  0),   # front slope start
        (100, 5),   # slope end
        (100, 15),  # back-top
        (20,  15),  # back-top step
        (20,  10),  # back step down
        (0,   10),  # front-top
    ])
    .close()
)

# Extrude the profile in Y to make the solid body
result = profile.extrude(10)

# Cut two long side grooves on the +Y face
groove_positions = [(30, 3), (60, 3)]
for x_pos, z_pos in groove_positions:
    result = (
        result
        .faces(">Y")
        .workplane()
        .center(x_pos - 50, z_pos - 5)  # center relative to face mid
        .rect(50, 1)                     # length 50 in X, depth 1 in Z
        .cutThruAll()
    )

# Chamfer the front vertical edges at X=0
result = result.edges("|X and >>Z").chamfer(1)

# Fillet the top back outer edge at the slope
result = result.edges(">Z and >>X").fillet(2)