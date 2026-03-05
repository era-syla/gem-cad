import cadquery as cq

# --- Dimensions & Parameters ---
thickness = 2.0

# Coordinates setup relative to an origin (0,0) at the "armpit" 
# (intersection of the top arm's bottom edge and the main body's left edge).

# Top Arm (extends Left and Up)
arm_len = 60.0
arm_height = 40.0
arm_tl = (-arm_len, arm_height)     # Top-Left
arm_bl = (-arm_len, 0.0)            # Bottom-Left

# Tab (protrudes from top of arm)
tab_width = 18.0
tab_height = 12.0
tab_x_offset = -30.0 # From origin (roughly aligned with arm/body junction)
tab_tl = (tab_x_offset, arm_height + tab_height)
tab_tr = (tab_x_offset + tab_width, arm_height + tab_height)

# Main Body (extends Right and Down)
body_width = 50.0
body_height_drop = 80.0 # How far down it goes
body_tr = (body_width, arm_height)
body_br = (body_width, -body_height_drop)
body_bl_start = (10.0, -body_height_drop) # Start of the bottom curve

# Spline Control Points for the "Hook/Head" shape at the bottom
# Curves from bottom of body back to origin (0,0)
spline_pts = [
    (0, -body_height_drop - 10),
    (-25, -body_height_drop - 15), # The "nose"
    (-20, -40),                    # The "throat"
    (0, 0)                         # Back to origin
]

# --- Geometry Construction ---

# 1. Base Solid
# Trace the outline Counter-Clockwise (starting from Arm Bottom Left)
result = (
    cq.Workplane("XY")
    .moveTo(*arm_bl)
    .lineTo(*arm_tl)
    .lineTo(tab_x_offset, arm_height)           # Start of tab
    .lineTo(*tab_tl)                            # Tab up
    .lineTo(*tab_tr)                            # Tab across
    .lineTo(tab_x_offset + tab_width, arm_height)# Tab down
    .lineTo(*body_tr)                           # Top edge of body
    .lineTo(*body_br)                           # Right edge of body
    .lineTo(*body_bl_start)                     # Bottom edge before hook
    .spline(spline_pts, includeCurrent=True)    # The organic hook shape
    .close()
    .extrude(thickness)
)

# 2. Add Fillets to the Tab
# Select edges near the top corners of the tab
result = result.edges(cq.NearestToPointSelector(tab_tl)).fillet(3.0)
result = result.edges(cq.NearestToPointSelector(tab_tr)).fillet(3.0)

# 3. Cut Holes
# Define hole positions and sizes
holes = [
    # (x, y, diameter)
    (tab_x_offset + tab_width/2, arm_height + tab_height/2, 6.0), # Tab Hole
    (-arm_len + 12, arm_height - 15, 3.5),                        # Left Arm Hole
    (-20, arm_height - 10, 3.5),                                  # Right Arm Hole
    (25, -10, 4.0),                                               # Main Body Hole
    (-12, -body_height_drop - 5, 3.5)                             # Hook/Nose Hole
]

workplane = result.faces(">Z").workplane()

for x, y, d in holes:
    workplane = workplane.pushPoints([(x, y)]).hole(d)

result = workplane

# 4. Cut Linear Slot
# Located below the tab area
slot_center = (-10, 25)
slot_length = 25.0
slot_width = 1.5

result = (
    result.faces(">Z")
    .workplane()
    .center(*slot_center)
    .slot2D(slot_length, slot_width, 0) # 0 degrees rotation
    .cutThruAll()
)

# Return the result for visualization
if 'show_object' in locals():
    show_object(result)