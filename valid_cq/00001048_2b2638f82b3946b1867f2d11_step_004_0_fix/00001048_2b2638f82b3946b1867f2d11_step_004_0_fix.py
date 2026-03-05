import cadquery as cq

# Parameters for the tube
tube_outer = 20
tube_wall = 1.5
tube_height = 200

# Create a square tube by extruding and shelling
tube = (
    cq.Workplane("XY")
    .rect(tube_outer, tube_outer)
    .extrude(tube_height)
    .faces(">Z")
    .shell(-tube_wall)
)

# Parameters for the small L-bracket
bracket_thickness = 2
bracket_leg = 10
bracket_depth = 10

# Define the L-shaped cross section in the XZ plane, then extrude in Y
l_profile = [
    (0, 0),
    (0, bracket_leg),
    (bracket_thickness, bracket_leg),
    (bracket_thickness, bracket_thickness),
    (bracket_leg, bracket_thickness),
    (bracket_leg, 0),
    (0, 0),
]
bracket = (
    cq.Workplane("XZ")
    .polyline(l_profile)
    .close()
    .extrude(bracket_depth)
    .translate((30, 0, 0))
)

result = tube.union(bracket)