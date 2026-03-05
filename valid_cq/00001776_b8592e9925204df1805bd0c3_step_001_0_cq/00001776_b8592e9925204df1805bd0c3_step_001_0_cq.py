import cadquery as cq

# Define parametric dimensions
# Overall dimensions
overall_width = 100.0   # Total width (X-axis)
overall_depth = 40.0    # Total depth (Y-axis)
overall_height = 80.0   # Total height (Z-axis)

# Stair step dimensions
step1_height = 20.0     # Height of the lowest step
step2_height = 40.0     # Height of the middle step
step3_height = 60.0     # Height of the top step (not used directly, but implicit)

step_width = 25.0       # Horizontal run of each step

# Create the base block
# We start with a solid block and will cut away the "stairs"
result = cq.Workplane("XY").box(overall_width, overall_depth, overall_height)

# Define the cutting profile for the stairs
# We will draw a sketch on the side face (XZ plane essentially) and cut it out
# The profile needs to remove the material to form the steps.

# Let's align the Workplane to the front face to cut through
result = (
    result
    .faces(">Y")  # Select the front face (positive Y)
    .workplane()
    .center(overall_width/2, -overall_height/2) # Move origin to bottom-right corner of the face
)

# Draw the shape to remove
# We are starting from the bottom-right corner relative to the face
# We need to cut out the "empty space" above the steps.
# The geometry consists of vertical rises and sloped runs.

cut_profile = (
    result
    .moveTo(-step_width * 0.5, overall_height) # Start at top right corner, but slightly in to define the first cut
    # Actually, let's trace the "void" shape relative to the corner.
    # It's easier to create the step profile as a closed polygon and cut.
    
    # Resetting approach: Let's create the solid profile directly instead of cutting a box.
    # It is cleaner parametrically.
)

# --- REVISED APPROACH: Extrude the profile ---

# Define the points for the side profile (on XZ plane)
# Origin (0,0) is bottom-left corner
pts = [
    (0, 0),                         # Bottom-left
    (overall_width, 0),             # Bottom-right
    (overall_width, step1_height),  # Up to first step height
    (overall_width - step_width, step1_height), # Inward for first step
    # Note: The image shows SLOPED vertical faces for the steps, not purely vertical.
    # Let's assume a slight angle or make them vertical based on typical stair logic?
    # Looking closely at the image:
    # - The lowest step has a vertical riser.
    # - The second step has a vertical riser.
    # - The transition between steps looks slightly angled in the specific "sawtooth" way often found in dovetail guides, 
    #   BUT looking closer at the middle step, the vertical face seems perpendicular to the ground.
    #   However, there is a distinct sloped face on the *second* step down. 
    #   Let's look at the "cut" approach again.
    
    # Let's re-examine the image geometry.
    # It looks like a large block with a "staircase" cut into the right side.
    # Step 1 (bottom right): Flat top, vertical right face.
    # Step 2 (middle): Flat top, vertical right face.
    # Step 3 (top): Flat top.
    # WAIT, looking at the "vertical" parts of the steps.
    # The riser between the lowest step and the middle step is angled/sloped.
    # The riser between the middle step and the top block is also slightly angled/sloped.
]

# Let's define dimensions for the specific sloped risers shown in the image.
# It looks like a "dovetail" or angled guide slideway geometry.

base_width = 80.0
total_height = 60.0
depth = 30.0

# Coordinates for the profile on the XZ plane
# (0,0) is bottom-left
p0 = (0, 0)
p1 = (base_width, 0)
p2 = (base_width, 15.0)  # Height of first step
p3 = (65.0, 15.0)        # First step horizontal run
p4 = (55.0, 35.0)        # Angled riser up to second step
p5 = (40.0, 35.0)        # Second step horizontal run
p6 = (30.0, total_height) # Angled riser up to top
p7 = (0, total_height)    # Top left corner

result = (
    cq.Workplane("XZ")
    .polyline([p0, p1, p2, p3, p4, p5, p6, p7])
    .close()
    .extrude(depth)
)