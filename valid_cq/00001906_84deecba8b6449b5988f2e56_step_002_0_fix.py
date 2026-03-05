import cadquery as cq

# L-shaped corner bracket
# Dimensions estimated from image
thickness = 8
width = 60
arm_length = 60
corner_radius = 15
hole_diameter = 6
slot_width = 6
slot_length = 12

# Create the L-shape profile in XY plane, then extrude in Z
# The bracket lies flat - two arms meeting at 90 degrees

# Build the 2D profile of the L-bracket (top view)
# Outer dimensions: two arms each ~60mm long, ~60mm wide (the extrude height)
# Actually looking at image: it's a vertical bracket - two flat plates at 90 degrees
# Each arm: length ~60, height ~60, thickness ~8

# Let's build it as: 
# - Horizontal arm going in +X direction
# - Vertical arm going in +Y direction
# - Both have same cross-section (width x thickness)
# - Extrude in Z for the height

arm_w = 60  # length of each arm
height = 60  # height (extrude depth)
t = 8       # thickness of bracket plate

# 2D L-profile points (outer corner at origin)
# Going clockwise
pts = [
    (0, 0),
    (arm_w, 0),
    (arm_w, t),
    (t, t),
    (t, arm_w),
    (0, arm_w),
]

profile = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
)

# Extrude
bracket = profile.extrude(height)

# Add fillet on inner corner edge (the vertical inner corner)
# The inner corner is at (t, t) - fillet the inner vertical edge
bracket = bracket.edges("|Z").edges(cq.selectors.NearestToPointSelector((t, t, height/2))).fillet(corner_radius)

# Now add holes/slots to the faces

# Front face of horizontal arm (Y=0 face) - two holes
# The face at Y=0, from X=0 to X=arm_w, Z=0 to Z=height
front_face_holes = (
    bracket
    .faces(">Y").workplane(centerOption="CenterOfBoundBox")
)

# Face at Y=0 (the front of horizontal arm)
# Add circular holes on the front face (Y=0 plane)
bracket = (
    bracket
    .faces("<Y")
    .workplane(centerOption="CenterOfBoundBox")
    .pushPoints([(-15, 0), (15, 0)])
    .circle(hole_diameter / 2)
    .cutBlind(-t - 1)
)

# Face at X=arm_w (right end of horizontal arm) - slot holes
bracket = (
    bracket
    .faces(">X")
    .workplane(centerOption="CenterOfBoundBox")
    .pushPoints([(0, 10), (0, -10)])
    .slot2D(slot_length, slot_width, 0)
    .cutBlind(-t - 1)
)

# Face at Y=arm_w (top end of vertical arm) - one circular hole
bracket = (
    bracket
    .faces(">Y")
    .workplane(centerOption="CenterOfBoundBox")
    .circle(hole_diameter / 2)
    .cutBlind(-t - 1)
)

# Fillet top and bottom edges for cleaner look
bracket = (
    bracket
    .edges("|Z")
    .edges(cq.selectors.NearestToPointSelector((arm_w, arm_w/2, height/2)))
    .fillet(2)
)

result = bracket