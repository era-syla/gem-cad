import cadquery as cq

# --- Parametric Dimensions ---
# Main Body
height_body = 60.0
width_body = 40.0
depth_body = 30.0

# Wing (Flange)
height_wing = 25.0
width_wing = 50.0
fillet_radius = 15.0  # Fillet between body and wing

# Pocket (Recess)
pocket_width = 24.0
pocket_depth = 20.0
pocket_floor_height = 5.0
pocket_arc_center_z = 38.0

# Holes
center_hole_dia = 10.0
wing_hole_dia = 4.0
wing_hole_spacing_x = 24.0
wing_hole_spacing_z = 12.0

# --- Modeling ---

# 1. Create the base L-shaped profile
# We draw on the XZ plane (Front) and extrude along Y (Depth)
# Origin is at the bottom-left corner
base = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(width_body + width_wing, 0)         # Bottom edge
    .lineTo(width_body + width_wing, height_wing) # Wing right edge
    .lineTo(width_body, height_wing)            # Wing top edge
    .lineTo(width_body, height_body)            # Body right edge (upper)
    .lineTo(0, height_body)                     # Body top edge
    .close()
    .extrude(depth_body)
)

# 2. Add the structural fillet
# Select the inner edge between the tall body and the wing
# We select the edge closest to the theoretical corner point
fillet_selector = cq.NearestToPointSelector((width_body, depth_body / 2, height_wing))
base = base.edges(fillet_selector).fillet(fillet_radius)

# 3. Create the Pocket (U-shaped recess)
# We work on the front face (>Y) and cut inwards
# Using ProjectedOrigin to maintain X, Z coordinates relative to global origin
pocket_r = pocket_width / 2.0
pocket_center_x = width_body / 2.0

# Define points for the pocket path
p_start = (pocket_center_x - pocket_r, pocket_floor_height)
p_bot_right = (pocket_center_x + pocket_r, pocket_floor_height)
p_arc_start = (pocket_center_x + pocket_r, pocket_arc_center_z)
p_arc_top = (pocket_center_x, pocket_arc_center_z + pocket_r)
p_arc_end = (pocket_center_x - pocket_r, pocket_arc_center_z)

base = (
    base.faces(">Y").workplane(centerOption="ProjectedOrigin")
    .moveTo(*p_start)
    .lineTo(*p_bot_right)
    .lineTo(*p_arc_start)
    .threePointArc(p_arc_top, p_arc_end) # Create the top arch
    .close()
    .cutBlind(-pocket_depth)
)

# 4. Create the Center Hole
# Concentric with the pocket arc, cutting through the entire part
base = (
    base.faces(">Y").workplane(centerOption="ProjectedOrigin")
    .moveTo(pocket_center_x, pocket_arc_center_z)
    .circle(center_hole_dia / 2.0)
    .cutBlind(-depth_body)
)

# 5. Create Mounting Holes on the Wing
# Calculate center positions for the pattern
wing_center_x = width_body + (width_wing / 2.0)
wing_center_z = height_wing / 2.0

# Define the 4 hole locations
wing_holes = [
    (wing_center_x - wing_hole_spacing_x/2, wing_center_z - wing_hole_spacing_z/2),
    (wing_center_x + wing_hole_spacing_x/2, wing_center_z - wing_hole_spacing_z/2),
    (wing_center_x - wing_hole_spacing_x/2, wing_center_z + wing_hole_spacing_z/2),
    (wing_center_x + wing_hole_spacing_x/2, wing_center_z + wing_hole_spacing_z/2),
]

result = (
    base.faces(">Y").workplane(centerOption="ProjectedOrigin")
    .pushPoints(wing_holes)
    .circle(wing_hole_dia / 2.0)
    .cutBlind(-depth_body)
)