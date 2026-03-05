import cadquery as cq

# --- Parametric Dimensions ---

# Fuselage
fuselage_length = 120.0
fuselage_radius = 6.0

# Nose
nose_length = 25.0
nose_tip_radius = 2.0
tip_cap_length = 3.0

# Main Wings
wing_x_pos = 75.0        # X position of the wing root leading edge (from rear)
wing_span = 55.0         # Span from centerline to tip
wing_root_chord = 30.0
wing_tip_chord = 10.0
wing_sweep_back = 15.0   # Distance the tip LE is behind the root LE
wing_thickness = 1.5

# Tail Fins
tail_x_pos = 15.0        # X position of the tail root leading edge (from rear)
tail_span = 20.0         # Span from centerline
tail_root_chord = 15.0
tail_tip_chord = 6.0
tail_sweep_back = 5.0
tail_thickness = 1.5

# --- Modeling Steps ---

# 1. Create the main fuselage body (Cylinder aligned with X-axis)
fuselage = cq.Workplane("YZ").circle(fuselage_radius).extrude(fuselage_length)

# 2. Create the nose cone (Loft from fuselage body to tip radius)
nose_cone = (
    cq.Workplane("YZ")
    .workplane(offset=fuselage_length)
    .circle(fuselage_radius)
    .workplane(offset=nose_length)
    .circle(nose_tip_radius)
    .loft()
)

# 3. Create the nose tip cap (Small extrusion with fillet)
nose_tip = (
    cq.Workplane("YZ")
    .workplane(offset=fuselage_length + nose_length)
    .circle(nose_tip_radius)
    .extrude(tip_cap_length)
    .faces(">X").fillet(nose_tip_radius * 0.5)
)

# 4. Create Main Wings
# Define the 2D profile points for the right wing (on XY plane)
# X grows from rear (0) to front. 
wing_pts = [
    (wing_x_pos - wing_root_chord, fuselage_radius),    # Root Trailing Edge
    (wing_x_pos, fuselage_radius),                      # Root Leading Edge
    (wing_x_pos - wing_sweep_back, wing_span),          # Tip Leading Edge
    (wing_x_pos - wing_sweep_back - wing_tip_chord, wing_span) # Tip Trailing Edge
]

right_wing = (
    cq.Workplane("XY")
    .polyline(wing_pts)
    .close()
    .extrude(wing_thickness)
    .translate((0, 0, -wing_thickness / 2.0)) # Center the wing vertically
)

left_wing = right_wing.mirror("XZ")

# 5. Create Tail Fins (Cruciform configuration)
# Define profile points (same logic as wings)
tail_pts = [
    (tail_x_pos - tail_root_chord, fuselage_radius),
    (tail_x_pos, fuselage_radius),
    (tail_x_pos - tail_sweep_back, tail_span),
    (tail_x_pos - tail_sweep_back - tail_tip_chord, tail_span)
]

# Horizontal Fin (Right)
tail_horz = (
    cq.Workplane("XY")
    .polyline(tail_pts)
    .close()
    .extrude(tail_thickness)
    .translate((0, 0, -tail_thickness / 2.0))
)

# Vertical Fin (Top)
# Drawn on XZ plane, so Y coordinate in polyline maps to Global Z height
tail_vert = (
    cq.Workplane("XZ")
    .polyline(tail_pts)
    .close()
    .extrude(tail_thickness)
    .translate((0, -tail_thickness / 2.0, 0)) # Center horizontally
)

# Combine and mirror to get all 4 fins
tail_fins = (
    tail_horz
    .union(tail_horz.mirror("XZ"))
    .union(tail_vert)
    .union(tail_vert.mirror("XY"))
)

# 6. Combine all parts into the final result
result = (
    fuselage
    .union(nose_cone)
    .union(nose_tip)
    .union(right_wing)
    .union(left_wing)
    .union(tail_fins)
)