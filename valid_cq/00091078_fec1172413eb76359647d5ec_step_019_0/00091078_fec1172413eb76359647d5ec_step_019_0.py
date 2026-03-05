import cadquery as cq

# -----------------------------------------------------------------------------
# Parameters
# -----------------------------------------------------------------------------
# Plate dimensions
plate_length = 140.0
plate_width = 35.0
plate_thickness = 3.0

# Mounting holes
hole_diameter = 4.0
hole_margin_x = 6.0
hole_margin_y = 6.0

# Text parameters
# Note: Text string approximated from image analysis
text_string = "Sierra 677912" 
text_size = 14.0
text_depth = 0.5
font_name = "Arial"  # Standard sans-serif font

# -----------------------------------------------------------------------------
# Modeling
# -----------------------------------------------------------------------------

# 1. Create the base rectangular plate
# We center it on the XY plane for symmetry
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Add Mounting Holes
# Select the top face (Z positive) to establish the workplane
# Create a construction rectangle to define the centers of the 4 holes
# Cut the holes at the vertices of this rectangle
result = (
    result.faces(">Z")
    .workplane()
    .rect(plate_length - 2 * hole_margin_x, 
          plate_width - 2 * hole_margin_y, 
          forConstruction=True)
    .vertices()
    .hole(hole_diameter)
)

# 3. Add Engraved Text
# Select the top face again
# Use the text method to cut geometry into the face
# Negative distance combined with cut=True performs the subtraction
result = (
    result.faces(">Z")
    .workplane()
    .text(text_string, 
          fontsize=text_size, 
          distance=-text_depth, 
          font=font_name,
          cut=True)
)