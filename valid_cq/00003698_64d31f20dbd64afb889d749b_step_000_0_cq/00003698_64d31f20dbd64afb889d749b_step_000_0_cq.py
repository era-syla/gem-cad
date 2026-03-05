import cadquery as cq

# --- Parametric Dimensions ---
# Arm specifications
num_arms = 8
arm_length = 100.0  # From center to tip
arm_width = 15.0    # Outer width of the U-channel
arm_height = 20.0   # Height of the walls
wall_thickness = 1.5
base_thickness = 1.5

# Small notches along the bottom edges (visible in the image)
notch_width = 3.0
notch_height = 1.5
notch_spacing = 10.0

# --- Helper Function for a Single Arm ---
def create_arm():
    # 1. Create the main block (outer envelope)
    # Origin is at one end (center of the star), growing along +X
    arm_geo = (
        cq.Workplane("XY")
        .box(arm_length, arm_width, arm_height, centered=(False, True, False))
    )
    
    # 2. Hollow out the inside to create the U-channel
    # We want the hollow part to be open at the top and the start (center of star)
    # Cut box dimensions:
    # Length: arm_length - wall_thickness (keep end wall)
    # Width: arm_width - 2 * wall_thickness
    # Height: arm_height - base_thickness
    # Position: Start at X=0, Y=0, Z=base_thickness
    
    cut_length = arm_length - wall_thickness
    cut_width = arm_width - 2 * wall_thickness
    cut_height = arm_height - base_thickness
    
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=base_thickness)
        .box(cut_length, cut_width, cut_height, centered=(False, True, False))
    )
    
    arm_geo = arm_geo.cut(cutter)
    
    # 3. Create the notches along the bottom edges
    # We'll create a series of small boxes to subtract
    num_notches = int(arm_length / notch_spacing)
    
    # Create a sketch or solid for the notches
    # We need notches on both sides of the Y axis (Y = +/- arm_width/2)
    
    for side in [-1, 1]:
        y_pos = side * (arm_width / 2)
        
        # Center the cutter on the edge
        notch_cutter = (
            cq.Workplane("XY")
            .rarray(notch_spacing, 1, num_notches, 1) # Linear array along X
            .box(notch_width, notch_width, notch_height * 2, centered=(True, True, True))
            .translate((arm_length / 2, y_pos, 0)) # Move array to cover the arm length
        )
        arm_geo = arm_geo.cut(notch_cutter)
        
    return arm_geo

# --- Assembly Construction ---

# Create one arm instance
base_arm = create_arm()

# Initialize the result container
result = cq.Workplane("XY")

# Polar array logic: Rotate and union the arm `num_arms` times
for i in range(num_arms):
    angle = i * (360.0 / num_arms)
    rotated_arm = base_arm.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.union(rotated_arm)

# Clean up any potential artifacts from the central union (optional but good practice)
# In this specific geometry, the simple union works well because the open ends merge at the center.

# Export or visualization would happen here in a real script
# result.val().exportStep("star_maze.step")