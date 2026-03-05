import cadquery as cq

# ==============================================================================
# Parameters
# ==============================================================================
text_content = "CMU"
font_size = 50.0          # Height of the text
text_thickness = 10.0     # Depth of the extrusion (Z-axis)

# Slat/Louver configuration
# Controls the horizontal slicing effect
num_lines = 18            # Approximate number of horizontal lines covering the text height
slat_fill_ratio = 0.6     # Ratio of solid material to the pitch (0.0 to 1.0)

# Derived dimensions
bbox_width_est = font_size * 4.0  # Estimate width to ensure mask covers text
pitch = font_size / num_lines     # Distance between slat centers
slat_height = pitch * slat_fill_ratio # Height of the solid part of the slat
mask_z_depth = text_thickness * 2.0   # Oversized depth for clean boolean cut

# ==============================================================================
# Model Generation
# ==============================================================================

# 1. Generate the base 3D Text
# Creates the text geometry centered on the XY plane
text_obj = cq.Workplane("XY").text(
    text_content, 
    font_size, 
    text_thickness
)

# 2. Create the Slicing Mask (Grill)
# We generate a vertical array of horizontal rectangles (slats)
# The array is centered to align with the text center
mask_obj = (
    cq.Workplane("XY")
    .rarray(
        xSpacing=1,             # Spacing in X (irrelevant for xCount=1)
        ySpacing=pitch,         # Vertical spacing between slats
        xCount=1,               # Single column of slats
        yCount=num_lines + 6,   # Number of slats (padded to ensure coverage)
        center=True             # Center the array at origin
    )
    .rect(bbox_width_est, slat_height) # Create the slat profile
    .extrude(mask_z_depth)             # Extrude to 3D
    .translate((0, 0, -mask_z_depth/4)) # Shift down to ensure full Z-overlap
)

# 3. Apply Boolean Intersection
# Intersect the solid text with the slat mask to produce the final louvered text
result = text_obj.intersect(mask_obj)

# The 'result' variable now contains the final CadQuery object