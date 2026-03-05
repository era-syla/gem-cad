import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions
base_length = 80.0
base_width = 30.0
base_thickness = 5.0

# Central bridge (raised section)
bridge_height = 10.0  # Height from bottom of flanges to top of bridge
bridge_width = 25.0

# Central Cylinder
cyl_outer_diam = 25.0
cyl_inner_diam = 15.0
cyl_height = 25.0  # Height from top of bridge

# Ribs (Gussets)
rib_thickness = 4.0
rib_height = 15.0  # How high up the cylinder it goes
rib_length = 15.0  # How far out on the flange it goes

# --- Modeling Steps ---

# 1. Create the Base Profile
# The base looks like a flat plate with a raised center. We can sketch the side profile and extrude.
# Profile shape:
#   ______
#  |      |
# _|      |_
#
pts = [
    (-base_length/2, 0),
    (-bridge_width/2 - base_thickness, 0),  # Start of rise
    (-bridge_width/2 - base_thickness, bridge_height - base_thickness), # Up
    (-bridge_width/2, bridge_height - base_thickness), # In
    (-bridge_width/2, bridge_height), # Top corner
    (bridge_width/2, bridge_height), # Top
    (bridge_width/2, bridge_height - base_thickness), # Down corner
    (bridge_width/2 + base_thickness, bridge_height - base_thickness), # Out
    (bridge_width/2 + base_thickness, 0), # Down
    (base_length/2, 0), # End
    (base_length/2, base_thickness), # Thickness up
    (bridge_width/2 + base_thickness + base_thickness, base_thickness), # Back in
    (bridge_width/2 + base_thickness + base_thickness, bridge_height), # Back up
    (-bridge_width/2 - base_thickness - base_thickness, bridge_height), # Across top
    (-bridge_width/2 - base_thickness - base_thickness, base_thickness), # Back down
    (-base_length/2, base_thickness), # Back end
    (-base_length/2, 0) # Close
]

# A simpler approach for the base is to make the general shape solid and cut the slot.
# Let's try: A main block + two side flanges? 
# Or better: Extrude a "U" shape profile.

# Let's redefine the base construction for cleaner CadQuery logic.
# Step 1a: Main rectangular base including the bridge height
base_block = cq.Workplane("XY").box(base_length, base_width, bridge_height)

# Step 1b: Cut the side "shoulders" to make flanges
cut_width = (base_length - bridge_width - 2*base_thickness) / 2
cut_height = bridge_height - base_thickness

# Cut left shoulder
base_shape = base_block.faces(">Z").workplane() \
    .rect(base_length, base_width) \
    .cutBlind(-cut_height) # This just lowers the whole top, wrong approach.

# Let's stick to the profile extrusion method, it's robust for this specific cross-section.
# Drawing the profile on the XZ plane.
def base_profile_pts():
    h = bridge_height
    t = base_thickness
    w_bridge = bridge_width
    w_total = base_length
    
    x1 = w_bridge / 2.0
    x2 = x1 + t # vertical wall thickness location
    x3 = w_total / 2.0
    
    # Points traversing the perimeter clockwise starting from bottom-left
    return [
        (-x3, 0),       # Bottom left corner
        (-x2, 0),       # Start of vertical rise (outer)
        (-x2, h-t),     # Top of vertical rise (outer)
        (-x1, h-t),     # Inner edge of vertical rise
        (-x1, h),       # Top surface start
        (x1, h),        # Top surface end
        (x1, h-t),      # Inner edge (right)
        (x2, h-t),      # Top of vertical rise (right)
        (x2, 0),        # Bottom of vertical rise (right)
        (x3, 0),        # Bottom right corner
        (x3, t),        # Top of flange (right)
        (x2+t, t),      # Inner corner of flange (right) NOTE: assuming fillet-like straight connection for simplicity or 90 deg
                        # Actually, looking at the image, the wall thickness is constant.
                        # Let's just make the solid block shape and shell/cut it.
    ]

# Alternative Strategy: Union of Primitives
# 1. Central Box (Bridge)
center_box = cq.Workplane("XY").box(bridge_width + 2*base_thickness, base_width, bridge_height)
# 2. Side Flanges
left_flange = cq.Workplane("XY").center(-(bridge_width/2 + base_thickness + (base_length/2 - (bridge_width/2 + base_thickness))/2), 0).box((base_length - (bridge_width + 2*base_thickness))/2, base_width, base_thickness)
right_flange = cq.Workplane("XY").center((bridge_width/2 + base_thickness + (base_length/2 - (bridge_width/2 + base_thickness))/2), 0).box((base_length - (bridge_width + 2*base_thickness))/2, base_width, base_thickness)

base_solid = center_box.union(left_flange).union(right_flange)
# Move base to sit on Z=0
base_solid = base_solid.translate((0, 0, bridge_height/2)) # Start centered at Z=0, now bottom is at Z=bridge_height/2 - bridge_height/2 ??? No.
# Box creates centered at origin.
# Center Box: Z range [-bridge_height/2, bridge_height/2]. We want [0, bridge_height]
center_box = cq.Workplane("XY").box(bridge_width + 2*base_thickness, base_width, bridge_height).translate((0,0,bridge_height/2))
# Flanges: Z range [-t/2, t/2]. We want [0, t]
flange_len = (base_length - (bridge_width + 2*base_thickness)) / 2
left_flange = cq.Workplane("XY").box(flange_len, base_width, base_thickness).translate((-base_length/2 + flange_len/2, 0, base_thickness/2))
right_flange = cq.Workplane("XY").box(flange_len, base_width, base_thickness).translate((base_length/2 - flange_len/2, 0, base_thickness/2))

base = center_box.union(left_flange).union(right_flange)

# Cut the channel underneath
base = base.faces("<Z").workplane().rect(bridge_width, base_width).cutBlind(bridge_height - base_thickness)

# 2. Create the Cylinder
# Sits on top of the bridge (Z = bridge_height)
cylinder = cq.Workplane("XY").workplane(offset=bridge_height) \
    .circle(cyl_outer_diam / 2).extrude(cyl_height)

# Hole through cylinder and base
combined_body = base.union(cylinder)
final_body = combined_body.faces(">Z").workplane().hole(cyl_inner_diam)

# 3. Create the Ribs
# Ribs connect the cylinder to the flanges.
# We will sketch on the XZ plane (front view) and extrude symmetrically.

# Define rib profile
# Start at top of flange, against the "bridge" wall
rib_start_x = bridge_width/2 + base_thickness
rib_start_z = base_thickness

# End point on flange
rib_end_x = rib_start_x + rib_length
rib_end_z = base_thickness

# Top point on cylinder
# The rib seems to attach to the cylinder wall above the bridge
rib_top_x = cyl_outer_diam / 2
rib_top_z = bridge_height + rib_height

# We need a robust way to attach. The rib goes from the flat flange to the vertical cylinder.
# The "bridge" wall is at x = bridge_width/2 + base_thickness.
# The cylinder wall is at x = cyl_outer_diam/2.
# Since cyl_outer_diam (25) < bridge width (25) + 2*thick (10) = 35, the cylinder is inside the bridge width.
# The rib has to bridge the gap over the "bridge" shoulder.

# Let's just make a triangular shape that intersects everything and union it.
rib_pts = [
    (rib_start_x, base_thickness), # Corner of flange and bridge wall
    (rib_end_x, base_thickness),   # Out on the flange
    (cyl_outer_diam/2, bridge_height + 10.0), # Up on the cylinder. 10.0 is arbitrary visual height
    (cyl_outer_diam/2, bridge_height) # At the base of the cylinder
]
# Wait, looking at the image, the rib is triangular.
# It starts on the flange surface.
# It ends up on the side of the cylinder.
# It crosses over the "step" of the bridge.

# Let's create a Workplane on XZ to draw the rib profile.
rib = cq.Workplane("XZ").workplane(offset=-rib_thickness/2) # Center the drawing plane? No, extrude creates thickness.
# We will draw on XZ (y=0) and extrude symmetric.

# Points for the right side rib
# (X, Z)
r_pts = [
    (cyl_outer_diam/2, bridge_height + 10.0),  # Top point on cylinder
    (base_length/2 - 5.0, base_thickness),      # Bottom point on flange (approximate based on visual)
    (cyl_outer_diam/2, base_thickness),         # Back corner (inside the solid, for full intersection)
]
# Refine points based on visual
# The rib touches the flange. Let's say it starts 5mm from edge.
rib_toe_x = base_length/2 - 5.0
rib_top_z = bridge_height + 12.0 # Height of rib tip

# To ensure clean union, we extend the rib geometry into the existing solid
rib_inner_x = 0.0 # Go all the way to center to be safe? No, just passed the cylinder wall.

right_rib = cq.Workplane("XZ") \
    .moveTo(rib_toe_x, base_thickness) \
    .lineTo(cyl_outer_diam/2, rib_top_z) \
    .lineTo(0, rib_top_z) \
    .lineTo(0, base_thickness) \
    .close() \
    .extrude(rib_thickness/2, both=True) # Extrude symmetric Y

# Mirror for left rib
left_rib = right_rib.mirror("YZ")

# Combine everything
result = final_body.union(right_rib).union(left_rib)

# Add fillets to make it look like the image (molded part)
# Fillet the junction between cylinder and bridge
# result = result.edges(cq.selectors.RadiusNthSelector(0)).fillet(1.0) 
# Automatic selection is tricky. Let's grab specific edges.

# Cylinder to Bridge Top fillet
result = result.edges(cq.NearestToPointSelector((0, cyl_outer_diam/2, bridge_height))).fillet(1.0)

# Rib vertical edges? Maybe not needed for exact replication, but good for "molded" look.
# The image shows fillets at the base of the ribs.
# Let's skip complex fillets to ensure stability of the script, 
# but adding the cylinder root fillet is prominent in the image.

# Re-establishing 'result' for the final output
result = result