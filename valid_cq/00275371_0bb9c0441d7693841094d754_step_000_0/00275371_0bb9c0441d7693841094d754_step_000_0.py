import cadquery as cq

# --- Parameters ---
# Handle dimensions
handle_length = 65.0
handle_radius = 6.0
bolster_height = 5.0
bolster_radius = 7.0

# Blade and Frame dimensions
blade_thickness = 2.5
total_height = 100.0  # Height of the metal part above the bolster
frame_width_half = 12.0  # Half width of the frame (left/right)
frame_spine_x = -10.0
frame_front_x = 10.0
cutout_gap = 2.5  # Gap between frame and blade

# --- Modeling ---

# 1. Handle
# Create cylinder on XY plane, extending downwards
handle = (
    cq.Workplane("XY")
    .workplane(offset=-bolster_height)
    .circle(handle_radius)
    .extrude(-handle_length)
    .edges("<Z")
    .fillet(handle_radius - 0.5) # Rounded bottom
)

# 2. Bolster (Collar)
# Sits at the origin (Z=0 to -bolster_height)
bolster = (
    cq.Workplane("XY")
    .workplane(offset=-bolster_height)
    .circle(bolster_radius)
    .extrude(bolster_height)
    .edges(">Z")
    .fillet(1.0)
)

# 3. Frame Geometry
# Drawn on XZ plane, extruded in Y (thickness)
frame_outer_pts = [
    (frame_spine_x, 0),                 # Bottom Left
    (frame_spine_x, total_height),      # Top Left (Spine tip)
    (frame_front_x, total_height - 20), # Top Right (Nose)
    (frame_front_x, 0)                  # Bottom Right
]

# Define the outer shape of the frame
frame_outer = (
    cq.Workplane("XZ")
    .moveTo(frame_outer_pts[0][0], frame_outer_pts[0][1])
    .lineTo(frame_outer_pts[1][0], frame_outer_pts[1][1])
    # Arc for the top curve
    .threePointArc((0, total_height - 3), frame_outer_pts[2])
    # Curve down the front
    .spline([(frame_front_x + 1, total_height/2), frame_outer_pts[3]], includeCurrent=True)
    .close()
    .extrude(blade_thickness/2, both=True)
)

# Define the cutout to create the frame loop
# We inset the outer points manually to ensure uniform-ish wall thickness
cutout_bottom_z = 15.0
cutout_pts = [
    (frame_spine_x + 3, cutout_bottom_z),
    (frame_spine_x + 3, total_height - 3),
    (frame_front_x - 3, total_height - 22),
    (frame_front_x - 3, cutout_bottom_z)
]

cutout = (
    cq.Workplane("XZ")
    .moveTo(cutout_pts[0][0], cutout_pts[0][1])
    .lineTo(cutout_pts[1][0], cutout_pts[1][1])
    .threePointArc((0, total_height - 6), cutout_pts[2])
    .lineTo(cutout_pts[3][0], cutout_pts[3][1])
    .close()
    .extrude(blade_thickness/2, both=True)
)

# Create the hollow frame
frame = frame_outer.cut(cutout)

# 4. Blade Geometry
# Sits inside the cutout
blade_stem_width = 4.0
blade_spine_x = -4.0
blade_edge_x = 4.0
blade_tip_z = total_height - 10.0
blade_base_z = cutout_bottom_z + 5.0 # Where blade body starts

blade = (
    cq.Workplane("XZ")
    .moveTo(blade_stem_width/2, 0) # Start at bottom center (connection to bolster)
    # S-curve stem for the edge side
    .spline([(blade_stem_width/2 + 1, 8), (blade_edge_x, blade_base_z)], includeCurrent=True)
    # Blade Edge
    .spline([(blade_edge_x, 60), (0, blade_tip_z)], includeCurrent=True)
    # Blade Spine
    .spline([(blade_spine_x, 60), (blade_spine_x, blade_base_z)], includeCurrent=True)
    # S-curve stem for the spine side
    .spline([(-blade_stem_width/2 - 1, 8), (-blade_stem_width/2, 0)], includeCurrent=True)
    .close()
    .extrude(blade_thickness/2, both=True)
)

# 5. Assembly
result = handle.union(bolster).union(frame).union(blade)
