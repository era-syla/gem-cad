import cadquery as cq

# --- Parameters ---

# Panel Dimensions
panel_width = 400.0
panel_height = 300.0
panel_thickness = 10.0

# Aluminum Extrusion Dimensions (approximating 2020 T-slot)
profile_size = 20.0
profile_length_long = 600.0
profile_length_short = 400.0

# Central Mechanism Housing (Simplified as a box with mounting features)
housing_width = 60.0
housing_depth = 60.0
housing_height = 80.0
wall_thickness = 3.0

# --- Helper Functions ---

def create_2020_profile(length):
    """
    Creates a simplified representation of a 2020 aluminum extrusion.
    """
    profile = (
        cq.Workplane("XY")
        .rect(profile_size, profile_size)
        .extrude(length)
    )
    
    # Add simple slots to make it look like extrusion
    slot_width = 6.0
    slot_depth = 3.0
    
    # Cut slots on all 4 faces
    slot_x = (
        cq.Workplane("XY")
        .rect(slot_width, profile_size + 2)
        .extrude(length)
    )
    slot_y = (
        cq.Workplane("XY")
        .rect(profile_size + 2, slot_width)
        .extrude(length)
    )
    
    # Add center hole
    center_hole = (
        cq.Workplane("XY")
        .circle(2.5)
        .extrude(length)
    )
    
    profile = profile.cut(slot_x).cut(slot_y).cut(center_hole)
    return profile

def create_mechanism_assembly():
    """
    Creates a simplified placeholder for the complex central mechanism 
    (motor mount/bracketry) seen in the image.
    """
    # Base block
    base = cq.Workplane("XY").box(housing_width, housing_depth, housing_height)
    
    # Side mounting plate (simplified bracket)
    bracket_plate = (
        cq.Workplane("YZ")
        .rect(housing_depth + 20, housing_height + 20)
        .extrude(wall_thickness)
        .translate((housing_width/2 + wall_thickness/2, 0, 0))
    )
    
    # A cylinder representing a motor or pivot
    pivot = (
        cq.Workplane("XZ")
        .circle(15)
        .extrude(housing_depth + 10)
        .translate((0, housing_depth/2, 0))
    )
    
    # Combine parts
    mech = base.union(bracket_plate).union(pivot)
    
    # Add some mounting holes pattern to the bracket to mimic the detailed look
    holes = (
        cq.Workplane("YZ")
        .rect(housing_depth, housing_height, forConstruction=True)
        .vertices()
        .circle(2.5)
        .extrude(wall_thickness * 2)
        .translate((housing_width/2, 0, 0))
    )
    
    mech = mech.cut(holes)
    return mech

# --- Geometry Construction ---

# 1. Create the Panel (Screen/Board)
# Positioned vertically
panel = (
    cq.Workplane("XZ")
    .rect(panel_width, panel_height)
    .extrude(panel_thickness)
    .translate((0, -panel_thickness/2, panel_height/2 + 50)) # Lifted up slightly
)

# 2. Create the Extrusions (Rails)
# Based on the image, there are rails on the left and right, and one central rail
rail_long = create_2020_profile(profile_length_long)
rail_short = create_2020_profile(profile_length_short)

# Left Rails (2 stacked/parallel)
left_rail_1 = rail_long.translate((-panel_width/2 - 50, -profile_length_long/2, 0))
left_rail_2 = rail_long.translate((-panel_width/2 - 100, -profile_length_long/2, 0))

# Right Rails (3 parallel)
right_rail_1 = rail_long.translate((panel_width/2 + 50, -profile_length_long/2, 0))
right_rail_2 = rail_long.translate((panel_width/2 + 100, -profile_length_long/2, 0))
right_rail_3 = rail_long.translate((panel_width/2 + 150, -profile_length_long/2, 0))

# Center Rail (perpendicular/under mechanism)
center_rail = (
    create_2020_profile(profile_length_short)
    .rotate((0,0,0), (0,0,1), 90) # Rotate to run Y-axis
    .translate((0, -profile_length_short/2, -profile_size))
)

# 3. Create the Mechanism
mechanism = create_mechanism_assembly()
# Position it at the bottom center of the panel
mechanism = mechanism.translate((0, 0, housing_height/2))

# --- Assembly ---

result = (
    panel
    .union(mechanism)
    .union(left_rail_1)
    .union(left_rail_2)
    .union(right_rail_1)
    .union(right_rail_2)
    .union(right_rail_3)
    .union(center_rail)
)

# Add colors for visual distinction if exported to STEP with color support
# (CadQuery logic handles geometry union, visual attributes are viewer dependent)