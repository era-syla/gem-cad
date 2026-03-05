import cadquery as cq

# --- Parameters ---
thickness = 2.0        # Plate thickness
slot_length = 30.0     # Central slot length
slot_width = 8.0       # Central slot width
hole_diameter = 4.5    # Diameter of the 3 screw holes

# --- Coordinates ---
# Derived based on visual proportions and geometric constraints
# Slope of top/bottom edges is approx 0.25 (14 degrees)

# Perimeter points (Counter-Clockwise starting from Bottom-Right)
p_br = (45, -11)       # Bottom Right corner
p_bl = (-35, -31)      # Bottom Left corner
p_vl = (-35, -5)       # End of vertical segment on the left
p_tl = (-22, 19.5)     # Start of top edge (end of left curve)
p_tr = (45, 36.25)     # Top Right corner

# Right Edge Notch (Semi-circle)
notch_center_y = 10
notch_r = 6.0
p_notch_top = (45, notch_center_y + notch_r)
p_notch_bot = (45, notch_center_y - notch_r)
p_notch_mid = (45 - notch_r, notch_center_y) # Inwards point

# Left Edge Blade Curve (Concave)
# Midpoint estimated to create a smooth concave blade profile
p_arc_left_mid = (-28, 7)

# Feature Positions
# Relative to origin (0,0) at slot center
holes_xy = [
    (-8, 16),   # Top Left
    (-8, -16),  # Bottom Left
    (35, 10)    # Right
]

# --- Geometry Construction ---

# 1. Base Sketch & Extrusion
# We draw the profile on the XY plane and extrude
base = (
    cq.Workplane("XY")
    .moveTo(*p_br)
    .lineTo(*p_bl)
    .lineTo(*p_vl)
    .threePointArc(p_arc_left_mid, p_tl) # Concave blade edge
    .lineTo(*p_tr)
    .lineTo(*p_notch_top)
    .threePointArc(p_notch_mid, p_notch_bot) # Right notch
    .lineTo(*p_br)
    .close()
    .extrude(thickness)
)

# 2. Create Cutting Tools (Slot & Holes)
# Defined on global XY to ensure absolute positioning accuracy
slot_tool = (
    cq.Workplane("XY")
    .slot2D(slot_length, slot_width)
    .extrude(thickness * 3)
    .translate((0, 0, -thickness)) # Center vertically relative to plate
)

holes_tool = (
    cq.Workplane("XY")
    .pushPoints(holes_xy)
    .circle(hole_diameter / 2)
    .extrude(thickness * 3)
    .translate((0, 0, -thickness))
)

# 3. Apply Cuts
result = base.cut(slot_tool).cut(holes_tool)

# 4. Optional: Add Blade Bevel (Chamfer)
# Select edges on the left side of the top face to simulate the blade edge
try:
    # Select the top face, then edges within the left bounding box
    result = (
        result.faces(">Z")
        .edges(cq.selectors.BoxSelector((-50, -50, 0), (-20, 50, 5)))
        .chamfer(0.8)
    )
except Exception:
    # If selection fails (e.g. topology changes), return the unchamfered solid
    pass
