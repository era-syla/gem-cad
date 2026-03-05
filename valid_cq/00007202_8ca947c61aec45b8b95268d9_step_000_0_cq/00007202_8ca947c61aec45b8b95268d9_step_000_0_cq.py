import cadquery as cq

# Parametric dimensions
# Overall dimensions of the block
length = 50.0   # Total length (or depth)
width = 20.0    # Thickness of the profile
height = 60.0   # Total height

# Dimensions of the cutout
cutout_height = 30.0  # Height of the opening
cutout_depth = 35.0   # Depth of the cut into the block
cutout_z_offset = 10.0 # Height from bottom where cutout starts

# Method 1: Create a base block and cut away the material
# Create the main rectangular prism
base = cq.Workplane("XY").box(length, width, height)

# Create a second shape to represent the negative space (the cutout)
# We position the cutout relative to the center of the base block
# The box is centered by default. 
# Base center is (0,0,0). 
# Top of base is z = height/2 = 30.
# Bottom of base is z = -height/2 = -30.
# Left face (where cut starts) is x = -length/2 = -25.
# Right face is x = length/2 = 25.

# We want to cut from the left side (-x direction) inwards.
# Let's align the cut.
cutout_center_z = -height/2 + cutout_z_offset + cutout_height/2
cutout_center_x = -length/2 + cutout_depth/2 

# Perform the cut
result = (
    base
    .faces("<X") # Select the negative X face
    .workplane()
    .center(0, cutout_z_offset + cutout_height/2 - height/2) # Move center to cutout center relative to face
    .rect(width, cutout_height) # Rectangle for the cut profile (on the YZ plane effectively)
    .cutBlind(cutout_depth) # Cut into the material
)

# Alternative simpler approach for clarity if needed, recreating 'result' entirely:
# Create a 2D profile on the XZ plane and extrude along Y (width)
# Coordinates relative to bottom-left corner (0,0)
pts = [
    (0, 0),
    (length, 0),
    (length, height),
    (0, height),
    (0, height - (height - cutout_height - cutout_z_offset)), # Top of cutout
    (length - (length - cutout_depth), height - (height - cutout_height - cutout_z_offset)), # Inner top corner
    (length - (length - cutout_depth), cutout_z_offset), # Inner bottom corner
    (0, cutout_z_offset), # Bottom of cutout
    (0,0) # Close shape
]

# Let's stick to the subtractive boolean method as it's often more robust for simple modifications
# Re-defining using a clean, easily adjustable logic

L = 50.0  # Length along X
W = 20.0  # Width along Y
H = 60.0  # Height along Z

# Cutout parameters
cut_depth = 30.0 # How deep the cut goes into X
cut_height = 20.0 # Height of the gap
cut_z_pos = 15.0  # Distance from bottom to start of cut

# Build
result = (
    cq.Workplane("XY")
    .box(L, W, H) # Create base block centered at origin
    .faces("-X") # Select the face at -X
    .workplane() 
    # Move origin to the bottom of the face (-H/2 in global Z)
    .center(0, -H/2) 
    # Move up to the center of the cut rectangle
    .center(0, cut_z_pos + cut_height/2)
    .rect(W + 2.0, cut_height) # Rectangle wider than part to ensure clean cut
    .cutBlind(-cut_depth) # Cut into the part (negative direction relative to workplane normal)
)