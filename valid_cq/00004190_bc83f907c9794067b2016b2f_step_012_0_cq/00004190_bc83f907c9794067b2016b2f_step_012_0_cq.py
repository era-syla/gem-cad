import cadquery as cq

# --- Parameter Definitions ---
table_length = 2000.0
table_width = 1000.0
table_thickness = 200.0

leg_height = 1000.0
leg_size = 50.0  # Square cross-section of the leg
foot_size = 100.0
foot_thickness = 10.0

brace_arm_length = 300.0  # Length along leg and along table
brace_thickness = 20.0    # Thickness of the triangular braces

# --- Helper Functions ---

def create_leg_assembly(x_pos, y_pos):
    """
    Creates a single leg with a foot and two triangular braces.
    x_pos, y_pos: Center position of the leg relative to origin.
    """
    
    # 1. The main vertical leg post
    leg = (
        cq.Workplane("XY")
        .rect(leg_size, leg_size)
        .extrude(-leg_height)
        .translate((x_pos, y_pos, 0))
    )
    
    # 2. The foot plate at the bottom
    foot = (
        cq.Workplane("XY")
        .rect(foot_size, foot_size)
        .extrude(foot_thickness)
        .translate((x_pos, y_pos, -leg_height))
    )
    
    # 3. Determine brace orientation based on quadrant
    # We want braces to point inwards along X and Y axes
    x_dir = -1 if x_pos > 0 else 1
    y_dir = -1 if y_pos > 0 else 1
    
    # Brace along X-axis
    # Create a triangular profile in the XZ plane
    pts_x = [
        (0, 0),
        (0, -brace_arm_length),
        (brace_arm_length * x_dir, 0)
    ]
    brace_x = (
        cq.Workplane("XZ")
        .polyline(pts_x)
        .close()
        .extrude(brace_thickness/2.0, both=True) # Extrude centered
        .translate((x_pos, y_pos, 0)) # Move to leg position (top of leg)
    )

    # Brace along Y-axis
    # Create a triangular profile in the YZ plane
    pts_y = [
        (0, 0),
        (0, -brace_arm_length),
        (brace_arm_length * y_dir, 0)
    ]
    brace_y = (
        cq.Workplane("YZ")
        .polyline(pts_y)
        .close()
        .extrude(brace_thickness/2.0, both=True) # Extrude centered
        .translate((x_pos, y_pos, 0)) # Move to leg position
    )
    
    return leg.union(foot).union(brace_x).union(brace_y)

# --- Main Geometry Construction ---

# 1. Create the Table Top
table_top = (
    cq.Workplane("XY")
    .rect(table_length, table_width)
    .extrude(table_thickness)
)

# 2. Calculate Leg Positions
# We place legs inset slightly from the edge
inset_x = table_length / 2.0 - leg_size * 2
inset_y = table_width / 2.0 - leg_size * 2

leg_positions = [
    (inset_x, inset_y),
    (inset_x, -inset_y),
    (-inset_x, inset_y),
    (-inset_x, -inset_y)
]

# 3. Create and Assemble Legs
legs_compound = None

for pos in leg_positions:
    leg_assy = create_leg_assembly(pos[0], pos[1])
    if legs_compound is None:
        legs_compound = leg_assy
    else:
        legs_compound = legs_compound.union(leg_assy)

# 4. Combine Top and Legs
result = table_top.union(legs_compound)

# If running in an environment that supports export or display:
# show_object(result) 
# result.exportStep("table_model.step")