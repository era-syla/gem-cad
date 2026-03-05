import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions
total_length = 220
wall_thickness = 2.0

# Mounting Plate (The flat tail feature)
plate_length = 60.0
plate_width = 30.0
plate_thickness = 4.0

# Main Aerodynamic Body Control Points
# Coordinates along X-axis
x_start = -15.0  # Where body merges with plate
x_belly = 80.0   # Widest part of the body
x_tip = 190.0    # The narrow tip

# Cross-section dimensions (Width, Depth)
# Depth is measured downwards from the Z=0 plane
dim_start = (30.0, 10.0)  # Width matches plate roughly, shallow depth
dim_belly = (42.0, 28.0)  # Wide and deep scoop
dim_tip = (12.0, 12.0)    # Circular tip

# --- Helper Functions ---

def create_u_profile(workplane, width, depth, top_extension=0.0):
    """
    Creates a U-shaped wire for lofting.
    :param width: Width at the top
    :param depth: Depth of the curve downwards
    :param top_extension: Extra height added to the top (used for the cutting tool)
    """
    w2 = width / 2.0
    
    # Points for the profile
    # Top-Left, Top-Right, Bottom-Center
    p_tl = (-w2, top_extension)
    p_tr = (w2, top_extension)
    p_b = (0, -depth)
    
    # Side intermediate points for a smooth organic curve (spline approximation)
    p_side_l = (-w2 * 0.85, -depth * 0.6)
    p_side_r = (w2 * 0.85, -depth * 0.6)

    # Create the wire
    # We use a spline for the bottom curve to get the aerodynamic shape
    wire = (workplane
            .moveTo(p_tl[0], p_tl[1])
            .lineTo(p_tr[0], p_tr[1])
            .spline([p_side_r, p_b, p_side_l], includeCurrent=True)
            .close()
           )
    return wire

# --- Geometry Construction ---

# 1. create the Mounting Plate
# Aligned such that the top surface is at Z=0, extending backwards along -X
plate = (cq.Workplane("XY")
         .center(-plate_length/2 - 10, 0)
         .box(plate_length, plate_width, plate_thickness)
         .translate((0, 0, -plate_thickness/2)) # Shift down so top is Z=0
        )

# 2. Create the Outer Shell (The Aerodynamic Body)
# We define planes perpendicular to the path (YZ planes along X)
wp_outer = cq.Workplane("YZ")

# Section 1: Transition area (merging with plate)
p1_outer = create_u_profile(
    wp_outer.workplane(offset=x_start), 
    dim_start[0], 
    dim_start[1]
)

# Section 2: Belly (Main volume)
p2_outer = create_u_profile(
    wp_outer.workplane(offset=x_belly), 
    dim_belly[0], 
    dim_belly[1]
)

# Section 3: Tip (Circular exit)
# We manually create a circle for the tip to ensure it's round
p3_outer = (wp_outer.workplane(offset=x_tip)
            .center(0, -dim_belly[1] * 0.4) # Align roughly with the scoop bottom line
            .circle(dim_tip[0] / 2.0)
           )

# Loft the sections to create the solid body
body_outer = p1_outer.add(p2_outer).add(p3_outer).loft(ruled=False)

# 3. Create the Inner Cutout (Hollow Scoop)
# This is a slightly smaller loft that will be subtracted
wp_inner = cq.Workplane("YZ")

# We start the cut slightly after the start to keep the plate solid where it joins
x_cut_start = x_start + 5.0

# Inner Section 1
p1_inner = create_u_profile(
    wp_inner.workplane(offset=x_cut_start), 
    dim_start[0] - wall_thickness*2, 
    dim_start[1] - wall_thickness,
    top_extension=5.0 # Extend up to cut through the top face (open canoe shape)
)

# Inner Section 2
p2_inner = create_u_profile(
    wp_inner.workplane(offset=x_belly), 
    dim_belly[0] - wall_thickness*2, 
    dim_belly[1] - wall_thickness,
    top_extension=5.0
)

# Inner Section 3 (Tip)
# We extend past the outer tip to ensure the hole goes all the way through
p3_inner = (wp_inner.workplane(offset=x_tip + 5.0)
            .center(0, -dim_belly[1] * 0.4)
            .circle((dim_tip[0] / 2.0) - wall_thickness)
           )

# Loft the inner sections
body_inner = p1_inner.add(p2_inner).add(p3_inner).loft(ruled=False)

# --- Final Assembly ---

# Union the plate and the outer body
main_solid = plate.union(body_outer)

# Subtract the inner core to create the hollow shell
result = main_solid.cut(body_inner)

# Apply a fillet to the junction between plate and body for smoothness
# We select edges that are vertical-ish around the join area
try:
    result = result.edges(cq.selectors.BoxSelector(
        (x_start - 10, -plate_width, -20),
        (x_start + 10, plate_width, 5)
    )).fillet(3.0)
except:
    # Fail-safe if selector finds no edges, geometry is still valid without fillet
    pass

# Export or display (for context, code ends with result variable)