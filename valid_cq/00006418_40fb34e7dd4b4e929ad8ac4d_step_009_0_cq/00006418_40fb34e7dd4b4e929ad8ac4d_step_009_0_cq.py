import cadquery as cq

# --- Parametric Dimensions ---
shaft_radius = 2.0       # Radius of the hexagonal cross-section for the main shaft
shaft_length = 100.0     # Total length of the vertical shaft
handle_radius = 4.0      # Radius of the hexagonal cross-section for the middle handle
handle_length = 25.0     # Length of the thicker middle section
arm_width = 3.0          # Width of the horizontal arm (rectangular cross-section)
arm_thickness = 10.0     # Height/Thickness of the horizontal arm
arm_length = 30.0        # Length of the horizontal arm extending from the shaft
arm_position_from_top = 10.0 # Distance from the top of the shaft to the arm

# --- Geometry Construction ---

# 1. Create the main vertical shaft
# Using a hexagonal polygon extruded vertically
shaft = (
    cq.Workplane("XY")
    .polygon(6, shaft_radius * 2)  # 6 sides, diameter = radius * 2
    .extrude(shaft_length)
)

# 2. Create the thicker middle section (handle)
# Centered vertically on the shaft
handle = (
    cq.Workplane("XY")
    .workplane(offset=(shaft_length - handle_length) / 2) # Start position
    .polygon(6, handle_radius * 2)
    .extrude(handle_length)
)

# 3. Create the horizontal arm
# It extends sideways near the top. Assuming rectangular cross-section based on visual.
arm = (
    cq.Workplane("XZ") # Draw on front plane to extrude sideways
    .workplane(offset=-arm_width/2) # Center the arm width relative to the shaft axis
    .moveTo(0, shaft_length - arm_position_from_top)
    .rect(arm_length * 2, arm_thickness, centered=False) # *2 and centered=False trick to start from center
    .extrude(arm_width)
    .translate((0, -arm_thickness/2, 0)) # Adjust vertical centering of the arm rectangle
)

# Refine arm position: The rect starts at (0, shaft_length - pos) and goes positive X and positive Z.
# Let's rebuild the arm more precisely.
# We want an arm sticking out in the +X direction.
arm = (
    cq.Workplane("YZ") # Plane perpendicular to X-axis
    .workplane(offset=0) # Start at the center axis
    .moveTo(0, shaft_length - arm_position_from_top)
    .rect(arm_width, arm_thickness) # Cross-section of the arm
    .extrude(arm_length) # Extrude along X
)

# Combine all parts
result = shaft.union(handle).union(arm)

# Export or visualization would happen here in a real script