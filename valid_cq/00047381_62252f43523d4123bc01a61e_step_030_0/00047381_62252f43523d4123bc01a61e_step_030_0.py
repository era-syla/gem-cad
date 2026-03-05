import cadquery as cq

# --- Parameters ---
thickness = 4.0        # Plate thickness
fillet_radius = 4.0    # Corner fillet radius
hole_diam = 3.5        # General mounting hole diameter

# Geometry dimensions (Estimated from image)
width_half = 110.0     # Total width 220
height_top = 260.0     # Height from main bottom edge to top
tab_depth = 40.0       # Depth of the bottom-left tab
chamfer_top_y = 80.0   # Y-coordinate where right chamfer starts
chamfer_bot_y = 40.0   # Y-coordinate where right chamfer ends
chamfer_inset_x = 80.0 # X-coordinate of the indented right section
tab_boundary_x = -65.0 # X-coordinate where the left tab starts

# --- 1. Define the Profile Points ---
# Coordinate System: Origin (0,0) is at the center of the plate width, aligned with the main bottom edge.
pts = [
    (width_half, height_top),      # Top Right
    (-width_half, height_top),     # Top Left
    (-width_half, -tab_depth),     # Bottom Left (Tab bottom)
    (tab_boundary_x, -tab_depth),  # Tab right bottom corner
    (tab_boundary_x, 0),           # Tab step up to main level
    (chamfer_inset_x, 0),          # Bottom Right main corner (start of right leg)
    (chamfer_inset_x, chamfer_bot_y), # Bottom of chamfer diagonal
    (width_half, chamfer_top_y)    # Top of chamfer diagonal
]

# --- 2. Create Base Body ---
# Create the main shape by extruding the polyline
result = cq.Workplane("XY").polyline(pts).close().extrude(thickness)

# --- 3. Apply Fillets ---
# Fillet all vertical edges (corners of the plate)
result = result.edges("|Z").fillet(fillet_radius)

# --- 4. Cut Bottom Notches ---
# Small rectangular cutouts on the bottom edge for clearance
notch_w = 12.0
notch_h_cut = 5.0 # Height of cut into the plate
# Create a cutter rectangle centered on the edge
notch_cutter = cq.Workplane("XY").rect(notch_w, notch_h_cut * 2).extrude(thickness)

# Cut Notch 1 (Left of center)
result = result.cut(notch_cutter.translate((-35, 0, 0)))
# Cut Notch 2 (Right of center)
result = result.cut(notch_cutter.translate((35, 0, 0)))


# --- 5. Create Hole Patterns ---

# Helper function for NEMA 17 Motor Mounts
# Standard NEMA 17: 31mm spacing, 22mm pilot hole
def cut_nema17(workplane, x, y):
    # Central Pilot Hole
    workplane = workplane.moveTo(x, y).circle(22.0 / 2).cutThruAll()
    # Mounting Screw Holes
    offset = 31.0 / 2
    mount_locs = [
        (x - offset, y - offset),
        (x + offset, y - offset),
        (x + offset, y + offset),
        (x - offset, y + offset)
    ]
    workplane = workplane.pushPoints(mount_locs).circle(3.2 / 2).cutThruAll()
    return workplane

# Cut Motor Mounts
# 1. Left Tab Mount (Lower)
result = cut_nema17(result, -87.5, -20.0)
# 2. Center Mount
result = cut_nema17(result, 0.0, 23.0)
# 3. Right Mount
result = cut_nema17(result, 60.0, 23.0)

# Cut General Mounting Holes
general_holes = [
    (-100, 250), # Top Left Corner
    (100, 250),  # Top Right Corner
    (-60, 160),  # Mid Left
    (100, 200),  # Mid Right (High near chamfer)
    (0, 100),    # Center Vertical Pair - Top
    (0, 80)      # Center Vertical Pair - Bottom
]

result = result.pushPoints(general_holes).circle(hole_diam / 2).cutThruAll()

# The 'result' variable now contains the final model