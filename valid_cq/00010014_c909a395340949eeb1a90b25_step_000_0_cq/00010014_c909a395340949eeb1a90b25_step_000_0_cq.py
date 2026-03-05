import cadquery as cq

# Parametric Dimensions
table_width = 800.0   # Total width of the table
table_depth = 500.0   # Total depth of the table
table_height = 400.0  # Total height from floor to top surface

# Main surface dimensions
plate_thickness = 20.0
shelf_height = 150.0   # Height of the upper box section
shelf_width = 250.0    # Width of the upper box section
shelf_wall_thickness = 20.0 # Wall thickness of the box

# Leg dimensions
leg_thickness = 20.0  # Thickness of the leg frame members
leg_width = table_depth # Legs span the full depth

# Derived dimensions
base_plate_width = table_width
base_plate_depth = table_depth

# --- Step 1: Create the main flat table surface ---
# This is the large flat plate at the bottom of the "L" shape of the top structure
main_plate = (
    cq.Workplane("XY")
    .box(base_plate_width, base_plate_depth, plate_thickness)
    .translate((0, 0, table_height - shelf_height - plate_thickness/2))
)

# --- Step 2: Create the upper box/shelf section ---
# Create the outer block
box_outer = (
    cq.Workplane("XY")
    .box(shelf_width, base_plate_depth, shelf_height)
    .translate((base_plate_width/2 - shelf_width/2, 0, table_height - shelf_height/2))
)

# Create the inner cut for the box
box_inner_cut = (
    cq.Workplane("XY")
    .box(shelf_width - 2*shelf_wall_thickness, base_plate_depth, shelf_height - 2*shelf_wall_thickness)
    .translate((base_plate_width/2 - shelf_width/2, 0, table_height - shelf_height/2))
)

# Create the hollow box
box_structure = box_outer.cut(box_inner_cut)

# --- Step 3: Create the Legs ---
# We need two rectangular frame legs.

def create_leg_frame():
    # Outer bounds of the leg frame
    frame_h = table_height - shelf_height
    frame_w = leg_width
    
    # Create the solid block first
    leg_block = (
        cq.Workplane("YZ")
        .box(frame_w, frame_h, leg_thickness)
    )
    
    # Create the cutout to make it a frame
    cutout_w = frame_w - 2 * leg_thickness
    cutout_h = frame_h - 2 * leg_thickness
    
    leg_cutout = (
        cq.Workplane("YZ")
        .box(cutout_w, cutout_h, leg_thickness)
    )
    
    frame = leg_block.cut(leg_cutout)
    return frame

# Generate one leg frame
leg_frame_geo = create_leg_frame()

# Position the left leg
left_leg = (
    leg_frame_geo
    .rotate((0,0,0), (0,0,1), 90) # Rotate to align with table width
    .translate((-base_plate_width/2 + leg_thickness/2, 0, (table_height - shelf_height)/2))
)

# Position the right leg
right_leg = (
    leg_frame_geo
    .rotate((0,0,0), (0,0,1), 90) # Rotate to align with table width
    .translate((base_plate_width/2 - leg_thickness/2, 0, (table_height - shelf_height)/2))
)

# --- Step 4: Combine all parts ---

# Note: The box structure overlaps with the main plate slightly in design intent usually to look monolithic,
# or sits on top. Based on the image, the box sits on top of the theoretical plane of the lower surface,
# effectively creating a "step".
# Let's union them all.

result = main_plate.union(box_structure).union(left_leg).union(right_leg)