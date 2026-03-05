import cadquery as cq

# --- Parameter Definitions ---
# Base dimensions
base_length = 80.0
base_width = 40.0
base_height = 5.0

# Main building block (left-most section)
b1_length = 20.0
b1_width = 18.0
b1_wall_height = 8.0
b1_roof_height = 5.0

# Middle taller section
b2_length = 25.0
b2_width = 24.0
b2_wall_height = 10.0
b2_roof_height = 8.0

# Right complex section
b3_length = 15.0
b3_width = 18.0
b3_wall_height = 8.0
b3_roof_height = 5.0

# --- Helper Functions ---
def make_house_profile(length, width, wall_h, roof_h):
    """
    Creates a simple extruded house shape (box + triangular prism roof)
    oriented along the X-axis.
    """
    # Create the rectangular body
    body = cq.Workplane("XY").box(length, width, wall_h)
    
    # Create the roof
    # We sketch the triangular profile on the side (YZ plane relative to the box)
    # But simpler in CadQuery is to create a wedge or loft.
    # Let's sketch the roof profile on the front face and extrude.
    
    # Vertices for the roof triangle (looking from the end)
    v1 = (-width/2.0, wall_h/2.0)
    v2 = (0.0, wall_h/2.0 + roof_h)
    v3 = (width/2.0, wall_h/2.0)
    
    # We extrude along X.
    roof = (
        cq.Workplane("YZ")
        .polyline([v1, v2, v3, v1])
        .close()
        .extrude(length)
    )
    
    # Combine
    combined = body.union(roof)
    return combined

def make_taller_house_profile(length, width, wall_h, roof_h):
    """
    Similar to the basic house, but maybe with the ridge running differently 
    or just larger parameters. The image shows the middle section ridge 
    aligned with the others (longitudinal).
    """
    # Create body
    body = cq.Workplane("XY").box(length, width, wall_h)
    
    # Create roof
    # Roof vertices on YZ plane
    v1 = (-width/2.0, wall_h/2.0)
    v2 = (0.0, wall_h/2.0 + roof_h)
    v3 = (width/2.0, wall_h/2.0)
    
    roof = (
        cq.Workplane("YZ")
        .polyline([v1, v2, v3, v1])
        .close()
        .extrude(length)
    )
    return body.union(roof)

# --- Construction ---

# 1. The Base Platform
base = cq.Workplane("XY").box(base_length, base_width, base_height)

# Calculate positions based on connecting them together
# We align them roughly centered on the base, but offset along X.

# Section 1 (Left)
part1 = make_house_profile(b1_length, b1_width, b1_wall_height, b1_roof_height)
# Move part1 up to sit on base
part1 = part1.translate((0, 0, base_height/2.0 + b1_wall_height/2.0))

# Section 2 (Middle - Taller/Wider)
part2 = make_taller_house_profile(b2_length, b2_width, b2_wall_height, b2_roof_height)
part2 = part2.translate((0, 0, base_height/2.0 + b2_wall_height/2.0))

# Section 3 (Right - Complex/Corner)
# Looking at the image, the rightmost part is perpendicular or has a side extension.
# It looks like a main block aligned with X, and a smaller side gable.
# For simplicity based on the isometric view, we will model the main right block
# and a secondary small extrusion.
part3_main = make_house_profile(b3_length, b3_width, b3_wall_height, b3_roof_height)
part3_main = part3_main.translate((0, 0, base_height/2.0 + b3_wall_height/2.0))


# Position calculations
# Center the assembly somewhat
# Left block center X
x1 = -b2_length/2.0 - b1_length/2.0
# Middle block center X is 0
x2 = 0
# Right block center X
x3 = b2_length/2.0 + b3_length/2.0

part1 = part1.translate((x1, 0, 0))
part3_main = part3_main.translate((x3, 0, 0))

# There is a small perpendicular protrusion on the right block in the image (a side gable).
# Let's add that.
side_gable_len = 8.0
side_gable_width = 8.0 # This becomes the length in X direction
side_gable_wall_h = 6.0
side_gable_roof_h = 3.0

# Create the side gable geometry (extruded along Y this time)
sg_body = cq.Workplane("XY").box(side_gable_width, side_gable_len, side_gable_wall_h)
# Roof for side gable (Triangle on XZ plane, extruded Y)
rv1 = (-side_gable_width/2.0, side_gable_wall_h/2.0)
rv2 = (0.0, side_gable_wall_h/2.0 + side_gable_roof_h)
rv3 = (side_gable_width/2.0, side_gable_wall_h/2.0)

sg_roof = (
    cq.Workplane("XZ")
    .polyline([rv1, rv2, rv3, rv1])
    .close()
    .extrude(side_gable_len)
)
side_gable = sg_body.union(sg_roof)

# Position the side gable attached to Part 3, sticking out towards -Y (front in isometric view)
# It sits on the base
sg_z_offset = base_height/2.0 + side_gable_wall_h/2.0
sg_y_offset = -b3_width/2.0 - side_gable_len/2.0 + 2.0 # Slight overlap
sg_x_offset = x3 

side_gable = side_gable.translate((sg_x_offset, sg_y_offset, sg_z_offset))


# --- Combine All Parts ---

structure = part1.union(part2).union(part3_main).union(side_gable)
result = base.union(structure)

# Offset alignment adjustments to match image closer (shifted towards one side of the base)
# The image shows the building flush with the "back" edge and some space in the "front".
shift_y = (base_width/2.0) - (b2_width/2.0) - 2.0
structure_shifted = structure.translate((0, shift_y, 0))

# Re-unite with base for final result
result = base.union(structure_shifted)