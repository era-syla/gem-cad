import cadquery as cq

# ==========================================
# Parameters
# ==========================================
length = 125.0          # Total vertical length
width_base = 22.0       # Width at the rounded bottom
thickness = 6.0         # Thickness of the part
fillet_radius = 2.5     # Radius for the top edge rounding

# Hole configuration
num_holes = 4
hole_dia = 3.5
csk_dia = 7.5
csk_angle = 82
hole_y_start = 20.0
hole_y_end = 100.0
hole_x_offset = -1.0    # Slight offset from center

# ==========================================
# Geometry Construction
# ==========================================

# Half-width at base for calculations
r = width_base / 2.0

# Define key points for the organic shape
# Coordinates are relative to the center of the bottom arc (0,0)

# Right Side (Back): Convex bottom, Concave neck, Flared top
pt_right_start = (r, 0)
pt_right_belly = (r + 1.5, length * 0.25)
pt_right_neck  = (r - 1.5, length * 0.65)
pt_right_top   = (r + 5.0, length) 

# Left Side (Front): Slightly curved, tapering in at top
pt_left_mid    = (-r - 1.0, length * 0.5)
pt_left_top    = (-r + 1.0, length - 12.0) # Lower Y to create angled top cut
pt_left_end    = (-r, 0)

# 1. Create the 2D Sketch Profile
sketch = (
    cq.Workplane("XY")
    .moveTo(*pt_right_start)
    # Spline up the right side
    .spline([pt_right_belly, pt_right_neck, pt_right_top], includeCurrent=True)
    # Straight line for the angled top edge
    .lineTo(*pt_left_top)
    # Spline down the left side
    .spline([pt_left_mid, pt_left_end], includeCurrent=True)
    # Closing semi-circle arc at the bottom
    .threePointArc((0, -r), pt_right_start)
    .close()
)

# 2. Extrude to create the base solid
solid = sketch.extrude(thickness)

# 3. Apply Fillets
# Fillet the edges of the top face (>Z) to achieve the rounded look
# We select the top face, then its edges
filleted_solid = solid.faces(">Z").edges().fillet(fillet_radius)

# 4. Drill Countersunk Holes
# Calculate hole spacing
y_spacing = (hole_y_end - hole_y_start) / (num_holes - 1)

result = filleted_solid
for i in range(num_holes):
    y_pos = hole_y_start + (i * y_spacing)
    result = (
        result.faces(">Z")
        .workplane()
        .moveTo(hole_x_offset, y_pos)
        .cskHole(hole_dia, csk_dia, csk_angle)
    )

# The final model is stored in the 'result' variable