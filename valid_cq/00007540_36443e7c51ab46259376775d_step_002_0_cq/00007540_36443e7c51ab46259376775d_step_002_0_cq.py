import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions of the plate
length = 60.0    # Total length
width = 30.0     # Total width (height in this orientation)
thickness = 5.0  # Plate thickness

# Corner notch dimensions
# The image shows notches at the four corners.
# Based on visual proportions:
notch_width = 5.0    # Depth of the cut from the side
notch_height = 5.0   # Height of the cut from top/bottom

# Central hole dimensions
hole_diameter = 6.0

# --- Modeling ---

# Start with the main rectangular block
# We orient it on the XY plane for simplicity
# Center=True keeps the origin at the geometric center, making symmetry easy
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
)

# Create the corner cutouts (notches)
# We need to subtract rectangular volumes from the four corners.
# We can do this by selecting the corners or by creating cutting boxes at specific coordinates.
# Let's use the coordinate approach for clarity and parametric robustness.

# Calculate offsets for the notch positions
x_pos = length / 2.0
y_pos = width / 2.0

# Create a list of points for the centers of the cutout boxes
# Note: box center position needs to be adjusted so the corner of the box aligns with the corner of the main part
# Actually, it's often easier to sketch the profile and extrude, or cut rectangles.
# Let's try the cut approach on the main face.

result = (
    result
    .faces(">Z")  # Select the top face
    .workplane()  # Create a workplane on top
    
    # Bottom-left corner notch
    .rect(notch_width * 2, notch_height * 2)  # Create a rectangle centered at origin (placeholder)
    .translate((-x_pos, -y_pos))              # Move to bottom-left corner
    
    # Bottom-right corner notch
    .rect(notch_width * 2, notch_height * 2)
    .translate((x_pos, -y_pos))
    
    # Top-right corner notch
    .rect(notch_width * 2, notch_height * 2)
    .translate((x_pos, y_pos))
    
    # Top-left corner notch
    .rect(notch_width * 2, notch_height * 2)
    .translate((-x_pos, y_pos))
    
    # Perform the cut through the entire thickness
    .cutThruAll()
)

# Add the central hole
result = (
    result
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)
)
