import cadquery as cq

# --- Parameters ---
height = 400.0
width = 80.0
thickness = 2.0
depth = 25.0

# Cutout / Profile Dimensions
narrow_width = 50.0
cut_width = width - narrow_width
cut_start_y = 120.0
cut_transition = 30.0
notch_w = 15.0
notch_h = 25.0

# Hole Dimensions
hole_large_dia = 12.0
hole_med_dia = 8.0
hole_small_dia = 4.5

# --- Geometry Construction ---

# 1. Base Extrusion (C-Channel Profile)
# Oriented: Length along Y, Width along X, Depth along Z
# Profile drawn on XZ plane
pts = [
    (0, depth), 
    (0, 0), 
    (width, 0), 
    (width, depth),
    (width - thickness, depth), 
    (width - thickness, thickness), 
    (thickness, thickness), 
    (thickness, depth)
]

# Extrude the profile to create the rail
# We stop slightly short of full height to represent the top flange thickness/bend area cleanly
base = cq.Workplane("XZ").polyline(pts).close().extrude(height - thickness)

# 2. Top Flange (Horizontal Cap/Bend)
# Modeled as a solid plate at the top
top_flange = (
    cq.Workplane("XY")
    .workplane(offset=height - thickness)
    .moveTo(width / 2, depth / 2)
    .rect(width, depth)
    .extrude(thickness)
)

# Union the base and the top flange
result = base.union(top_flange)

# 3. Side Profile Cutout
# Removes material from the left side to create the stepped profile
# Drawn on the front face (XY plane equivalent)
cut_poly = [
    (-10, height + 10),                            # Top Left (outside)
    (cut_width, height + 10),                      # Top Right of cut
    (cut_width, cut_start_y + cut_transition),     # Start of chamfer
    (0, cut_start_y),                              # End of chamfer
    (-10, cut_start_y)                             # Bottom Left (outside)
]

# Apply the cut through the entire depth
result = (
    result.faces("<Z")
    .workplane()
    .polyline(cut_poly)
    .close()
    .cutBlind(depth * 2)
)

# 4. Bottom Notch
# Cutout at the bottom-left corner
result = (
    result.faces("<Z")
    .workplane()
    .moveTo(0, 0)
    .rect(notch_w, notch_h, centered=False)
    .cutBlind(depth * 2)
)

# --- Holes ---

# Define hole positions (X, Y, Diameter)
# X is relative to the global origin (left edge of the original width)
# Hole line centered on the narrow section
center_line_x = cut_width + (narrow_width / 2.0)

face_holes = [
    # Top section
    (center_line_x, height - 40, hole_large_dia),
    (center_line_x, height - 100, hole_small_dia),
    (center_line_x, height - 150, hole_med_dia),
    (center_line_x, height - 200, hole_large_dia),
    (center_line_x, height - 250, hole_small_dia),
    
    # Bottom Wide Section
    # Left tab hole
    (25.0, 60.0, hole_large_dia),
    # Right bottom hole
    (width - 15.0, 40.0, hole_large_dia),
    
    # Small mounting holes (pairs)
    (33.0, 80.0, hole_small_dia),
    (33.0, 90.0, hole_small_dia),
    (width - 15.0, 60.0, hole_small_dia),
    (width - 15.0, 70.0, hole_small_dia),
]

# Apply holes to the main face
# We select the face at Z=0 (the web back face) and drill through
for x, y, d in face_holes:
    result = result.faces("<Z").workplane().moveTo(x, y).hole(d)

# Top Flange Holes
# 4 small holes on the top horizontal surface
top_hole_y_pos = depth / 2.0
top_hole_xs = [
    center_line_x - 15,
    center_line_x - 5,
    center_line_x + 5,
    center_line_x + 15
]

# Apply holes to the top face
for x in top_hole_xs:
    result = result.faces(">Y").workplane().moveTo(x, top_hole_y_pos).hole(hole_small_dia)

# Export or Render
# show_object(result) # Only used in CQ-editor context