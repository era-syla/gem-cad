import cadquery as cq

# --- Parametric Dimensions ---
height = 120.0        # Overall height of the plate
width = 34.0          # Overall width of the plate
thickness = 3.0       # Plate thickness
sagitta = 6.0         # Height of the convex curve at top and bottom

# Cutout parameters
left_cut_r = 11.0     # Radius of left side cutout
left_cut_y = 28.0     # Y position of left cutout
right_cut_r = 35.0    # Radius of right side cutout
right_cut_y = -15.0   # Y position of right cutout
right_cut_offset = 22.0 # Offset to make the right cut shallower

# Hole parameters
hole_dia = 3.5        # Diameter of the through holes
hole_pos_top = (-7.0, 45.0)
hole_pos_mid = (9.0, 5.0)
hole_pos_bot = (0.0, -48.0)

# --- Geometry Construction ---

# Define the corner points of the bounding rectangle
p_bl = (-width/2, -height/2) # Bottom-Left
p_tl = (-width/2, height/2)  # Top-Left
p_tr = (width/2, height/2)   # Top-Right
p_br = (width/2, -height/2)  # Bottom-Right

# Define arc mid-points for the top and bottom convex edges
p_top_arc = (0, height/2 + sagitta)
p_bot_arc = (0, -height/2 - sagitta)

# Create the base body with curved ends
base = (
    cq.Workplane("XY")
    .moveTo(*p_bl)
    .lineTo(*p_tl)                         # Left straight edge
    .threePointArc(p_top_arc, p_tr)        # Top convex arc
    .lineTo(*p_br)                         # Right straight edge
    .threePointArc(p_bot_arc, p_bl)        # Bottom convex arc
    .close()
    .extrude(thickness)
)

# Create the left cutout (deeper finger groove)
# Positioned on the left edge
base = base.cut(
    cq.Workplane("XY")
    .moveTo(-width/2, left_cut_y)
    .circle(left_cut_r)
    .extrude(thickness * 2, both=True)
)

# Create the right cutout (shallower, larger radius)
# Positioned on the right edge, offset outward to create a shallow arc
base = base.cut(
    cq.Workplane("XY")
    .moveTo(width/2 + right_cut_offset, right_cut_y)
    .circle(right_cut_r)
    .extrude(thickness * 2, both=True)
)

# Create the mounting holes
result = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints([hole_pos_top, hole_pos_mid, hole_pos_bot])
    .hole(hole_dia)
)