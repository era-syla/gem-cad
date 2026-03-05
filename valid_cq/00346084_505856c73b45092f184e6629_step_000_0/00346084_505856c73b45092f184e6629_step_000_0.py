import cadquery as cq

# --- Parameters ---
width = 30.0          # Width of the bracket
thickness = 5.0       # Material thickness
long_length = 80.0    # Length of the horizontal arm (outer dimension)
short_length = 50.0   # Length of the vertical arm (outer dimension)
hole_dia = 5.0        # Diameter of the screw hole
csk_dia = 10.0        # Diameter of the countersink
csk_angle = 90.0      # Countersink angle

# --- Model Construction ---

# 1. Base Geometry
# Create the horizontal arm aligned with X-axis
# Centered on Y (width) for symmetry, positioned from X=0
arm_horz = cq.Workplane("XY").box(long_length, width, thickness, centered=(False, True, False))

# Create the vertical arm aligned with Z-axis
# Centered on Y (width), positioned from X=0, Z=0
arm_vert = cq.Workplane("XY").box(thickness, width, short_length, centered=(False, True, False))

# Combine into L-shape
result = arm_horz.union(arm_vert)

# 2. Add Holes to Horizontal Arm
# Target the top face of the horizontal arm (Z = thickness)
# Note: The effective face starts at X = thickness after the union
face_center_x = (thickness + long_length) / 2.0

# Hole positions in global X coordinates
h1_x = 25.0
h2_x = 65.0

# Calculate offsets relative to the face center for the workplane
off1 = h1_x - face_center_x
off2 = h2_x - face_center_x

result = (
    result
    .faces(cq.NearestToPointSelector((long_length/2, 0, thickness)))
    .workplane()
    .pushPoints([(off1, 0), (off2, 0)])
    .cskHole(hole_dia, csk_dia, csk_angle)
)

# 3. Add Hole to Vertical Arm
# Target the inner face of the vertical arm (X = thickness)
# The face spans Z from thickness to short_length
face_center_z = (thickness + short_length) / 2.0

# We want the hole centered on the available flat area, which matches the face center
result = (
    result
    .faces(cq.NearestToPointSelector((thickness, 0, short_length/2)))
    .workplane()
    .pushPoints([(0, 0)])
    .cskHole(hole_dia, csk_dia, csk_angle)
)