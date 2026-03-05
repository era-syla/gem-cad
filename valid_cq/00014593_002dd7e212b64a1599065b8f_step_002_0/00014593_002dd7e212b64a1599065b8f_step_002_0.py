import cadquery as cq

# --- Parametric Dimensions ---
# Neck dimensions
neck_width = 10.0
neck_length = 100.0
neck_thickness = 3.0

# Headstock dimensions
head_length = 30.0
head_width_max = 24.0   # Width at the widest point (horns)
head_width_tip = 16.0   # Width at the tip
head_horn_pos_y = 12.0  # Distance from neck joint to horn
notch_depth = 5.0       # Depth of the V-cut at the tip

# Heel dimensions
heel_length = 15.0
heel_drop = 10.0        # Thickness added below the neck for the heel block
fillet_radius = 5.0     # Radius for the heel-to-neck transition

# --- Geometry Construction ---

# 1. Define points for the headstock profile (Right side)
# Coordinate system: Origin (0,0) is at the center of the neck/headstock junction.
# +Y is towards headstock, -Y is towards neck body.
pt_neck_joint = (neck_width / 2.0, 0)
pt_horn = (head_width_max / 2.0, head_horn_pos_y)
pt_tip = (head_width_tip / 2.0, head_length)
pt_notch = (0, head_length - notch_depth)

# 2. Create the main body (Neck + Headstock)
# We draw the outline on the XY plane and extrude downwards
main_body = (
    cq.Workplane("XY")
    .moveTo(neck_width / 2.0, -neck_length)        # Start at bottom-right of neck
    .lineTo(*pt_neck_joint)                        # Line up to neck joint
    
    # Headstock Right Side: Curve out to horn, then in to tip
    .spline([pt_horn, pt_tip], includeCurrent=True)
    
    # Headstock Tip: V-Notch
    .lineTo(*pt_notch)                             # Line to center notch
    
    # Headstock Left Side: Mirror geometry manually for the path
    .lineTo(-pt_tip[0], pt_tip[1])                 # Line out to left tip
    .spline([(-pt_horn[0], pt_horn[1]), (-pt_neck_joint[0], pt_neck_joint[1])], includeCurrent=True)
    
    .lineTo(-neck_width / 2.0, -neck_length)       # Line down left side of neck
    .close()                                       # Close the profile at bottom
    .extrude(-neck_thickness)                      # Extrude to create the board
)

# 3. Create the Heel
# A rectangular block added to the end of the neck on the bottom side
heel = (
    cq.Workplane("XY")
    .workplane(offset=-neck_thickness)             # Start at the bottom face of the neck
    .moveTo(0, -neck_length + heel_length / 2.0)   # Move center to heel position
    .rect(neck_width, heel_length)                 # Draw rectangle
    .extrude(-heel_drop)                           # Extrude downwards
)

# 4. Combine parts
result = main_body.union(heel)

# 5. Add Fillet
# Smooth transition where the heel block meets the neck thickness
# We select the edge at Z = -neck_thickness and Y = -neck_length + heel_length
edge_selector = cq.NearestToPointSelector((0, -neck_length + heel_length, -neck_thickness))
result = result.edges(edge_selector).fillet(fillet_radius)