import cadquery as cq

# Parametric dimensions
length = 400.0       # Total length of the angle
leg_width = 30.0     # Width of one leg of the L-shape
thickness = 3.0      # Thickness of the material
hole_diameter = 4.0  # Diameter of the through holes
hole_spacing = 50.0  # Distance between hole centers
start_offset = 25.0  # Offset from the end for the first hole
csk_diameter = 8.0   # Diameter of the countersink
csk_angle = 90.0     # Angle of the countersink

# Create the base L-profile
# We'll create a sketch on the YZ plane and extrude it along X
# The origin will be at the corner of the L

# Outer dimensions of the L
outer_w = leg_width
outer_h = leg_width

# Inner dimensions of the L (subtracted)
inner_w = leg_width - thickness
inner_h = leg_width - thickness

# Create the profile
# Points for the L-shape polygon
pts = [
    (0, 0),
    (0, outer_h),
    (thickness, outer_h),
    (thickness, thickness),
    (outer_w, thickness),
    (outer_w, 0),
    (0, 0)
]

# Create the base extrusion
base = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(length)
)

# Calculate hole positions
# We need holes on both flanges.
# Flange 1: The "vertical" one in the sketch (along Z in final orientation if extruding along X, but here on YZ plane extruded along X)
# Let's clarify orientation based on the extrude direction.
# The base is extruded along positive X.
# The "bottom" flange is on the XY plane (Z=0 to Z=thickness).
# The "vertical" flange is on the XZ plane (Y=0 to Y=thickness).

# Let's re-orient for clarity to match typical "L-bracket lying down"
# If we extrude along X:
# "Vertical" flange face normal is +Y.
# "Horizontal" flange face normal is +Z.
# However, the previous sketch `pts` defines an L shape where:
# - One leg goes up Y (from 0 to outer_h)
# - One leg goes along Z (from 0 to outer_w) - wait, workplane is YZ.
# Let's map coordinates: YZ plane. 
# pt (0,0) -> (0,0,0)
# pt (0, outer_h) -> (0, y=outer_h, z=0)
# pt (outer_w, 0) -> (0, y=0, z=outer_w)
# Extrude along X.
# So we have a flange on the XY plane (width=outer_w) and a flange on the XZ plane (height=outer_h).

# Let's calculate hole centers along the length (X-axis)
num_holes = int((length - 2 * start_offset) / hole_spacing) + 1
hole_x_locs = [start_offset + i * hole_spacing for i in range(num_holes)]

# Define hole position on the flanges
# The holes are centered on the flange width.
# Flange width is `leg_width`. Center is `leg_width / 2`.
# However, we need to be careful about which face we select.

# Select the top face of the bottom flange (normal = +Y, if drawn on XZ plane and extruded Y... wait, let's stick to the code above).
# Code above: Workplane("YZ").polyline(pts).extrude(length)
# Sketch points: (0,0) -> (0, leg_width) -> ... -> (leg_width, 0)
# Y coord goes 0 to 30. Z coord goes 0 to 30.
# Extrusion is along X.
# Bottom flange is roughly parallel to XY plane? No, let's look at points again.
# pts = [(0, 0), (0, outer_h), (thickness, outer_h), (thickness, thickness), (outer_w, thickness), (outer_w, 0), (0, 0)]
# Y coordinate corresponds to vertical in the 2D sketch.
# Z coordinate corresponds to horizontal in the 2D sketch (implied X in sketch, but workplane is YZ).
# Let's trace it carefully:
# Workplane("YZ") means local X is global Y, local Y is global Z.
# polyline points are (local_x, local_y).
# (0,0) -> Y=0, Z=0
# (0, outer_h) -> Y=0, Z=outer_h
# ...
# This creates an L where one leg is along Z axis and one leg is along Y axis.
# Extrusion is along global X.

# So we have:
# Leg 1: Flat on XY plane (Face normal +Z). Extends in Y direction.
# Leg 2: Flat on XZ plane (Face normal +Y). Extends in Z direction.
# Wait, checking the polyline again:
# (0,0) -> (0, 30) : Line along Local Y (Global Z). So this leg is vertical (XZ plane).
# (30, 0) : Line along Local X (Global Y). So this leg is horizontal (XY plane).

# We want to drill holes on the outer faces.
# Face 1: The "vertical" leg outer face. Normal is -Y (if drawn at x=0, y=0) or +Y depending on side.
# Looking at the points: (0,0) to (0, outer_h). This line is on X=0 (start of extrude). 
# Wait, let's simplify selection.
# We will select faces by normal vector or location.

# Let's find the holes centers.
# Center of "Horizontal" leg (on XY plane, thickness Z): Y = leg_width / 2
# Center of "Vertical" leg (on XZ plane, thickness Y): Z = leg_width / 2

# Using the image, holes are staggered or aligned?
# They look aligned in pairs at the same X coordinate.

# Process:
# 1. Create base
# 2. Select face of one leg, add holes.
# 3. Select face of other leg, add holes.

# Re-creating base for easier face selection orientation:
# Let's align L-shape such that the corner is at origin, extending +X, +Y, +Z.
# Base profile on YZ plane.
# Leg 1 goes along +Y (height leg_width, thickness).
# Leg 2 goes along +Z (width leg_width, thickness).
# Extrude +X.

result = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),
        (0, leg_width),
        (thickness, leg_width),
        (thickness, thickness),
        (leg_width, thickness),
        (leg_width, 0),
        (0, 0)
    ])
    .close()
    .extrude(length)
)

# Add holes to the "vertical" leg (the one extending in +Y, face normal +Z or -Z... wait)
# The leg along Y has faces with normals +/- X (ends), +/- Z (surfaces), +/- Y (edges).
# The large flat face we want to drill is parallel to XY plane.
# Wait, my coordinate tracing was:
# pts = (local_x, local_y). Workplane("YZ") -> local_x=Y, local_y=Z.
# (0,0) -> (0, leg_width) in local coords means (Y=0, Z=0) to (Y=0, Z=leg_width).
# So the leg going "up" in local coords (Z) is the vertical leg.
# The leg going "right" in local coords (Y) is the horizontal leg.

# Let's verify standard CadQuery Workplane orientation:
# Workplane("YZ"): Plane normal is X. Local X is Y axis. Local Y is Z axis.
# Point (0, leg_width) -> global Y=0, global Z=leg_width.
# Point (leg_width, 0) -> global Y=leg_width, global Z=0.
# So:
# Leg A: Along global Z axis. Inner face normal -Y, outer face normal +Y? No, thickness is in Y direction for this leg?
# Let's check points again:
# (0,0), (0, 30), (3, 30), (3, 3).
# Local X=0..3 (Global Y), Local Y=0..30 (Global Z).
# This is a leg standing up in Z, with thickness in Y.
# Face to drill is on the side, parallel to XZ plane. Normal is +Y or -Y.
# Since points go (0,0) to (0,30), this edge is at Y=0.
# The thickness goes to Y=3.
# So the outer face is at Y=0 (normal -Y) or inner face at Y=3?
# The polygon is drawn CCW. (0,0)->(0,30)->(3,30).
# So the bulk is in positive Y and positive Z.
# The face at Y=0 is the "back" of the leg.
# We want to drill into the face.
# Let's put holes on the face at Y=0 (the outer face of the vertical leg).
# Hole locations: X = various, Z = leg_width / 2.
# Actually, typically holes are centered on the flat part.
# The leg length is `leg_width`. The "flat" part accessible for a hole is roughly `leg_width - thickness` inside, but on the outside it's `leg_width`.
# Center for hole: `leg_width / 2` from the corner.

# Leg B: Along global Y axis (Local X).
# Points (3,3) -> (30, 3) -> (30, 0) -> (0,0).
# Bulk is in Y=0..30, Z=0..3.
# This is a leg lying along Y.
# Thickness is in Z.
# Face at Z=0 is the bottom. Face at Z=3 is the top (inside).
# Let's drill from the outside face (Z=0).
# Center for hole: Y = leg_width / 2.

# Operations
# Select Face Normal -Y (XZ plane side) -> Drill holes
# Select Face Normal -Z (XY plane bottom) -> Drill holes

# NOTE: The image shows countersinks. Countersinks are usually on the "outer" face so the screw head sits flush.
# The "outer" faces are Y=0 and Z=0 based on my polyline construction starting at 0,0 and going positive.
# So we select faces with normal (-1, 0, 0) ?? No, normal -Y is (0, -1, 0).
# And normal -Z is (0, 0, -1).

# Let's build the lists of points for the holes
# For the leg along Z (Face normal -Y): Points in (X, Z) plane
# Center line height Z = leg_width / 2
holes_leg_Z = [(x, leg_width / 2) for x in hole_x_locs]

# For the leg along Y (Face normal -Z): Points in (X, Y) plane
# Center line width Y = leg_width / 2
holes_leg_Y = [(x, leg_width / 2) for x in hole_x_locs]

# Apply operations
result = result.faces("<Y").workplane().pushPoints(holes_leg_Z).cskHole(hole_diameter, csk_diameter, csk_angle)
result = result.faces("<Z").workplane().pushPoints(holes_leg_Y).cskHole(hole_diameter, csk_diameter, csk_angle)

# Note on orientation in the image:
# The image shows the angle iron with the corner pointing towards the viewer/down.
# The outer faces are visible.
# Our model (extruding +X, legs +Y and +Z) has the corner at (X,0,0).
# Faces <Y and <Z are the outer faces. This matches the logic.