import cadquery as cq

# --- Parametric Dimensions ---
length = 80.0           # Total length of the part (X axis)
width = 40.0            # Total width of the part (Y axis)
height = 30.0           # Total height of the part (Z axis)

# Step/Cutout parameters
narrow_width = 20.0     # Width of the narrower section
step_length = 40.0      # Length of the narrow section (from one end)

# Feature parameters
fillet_radius = 5.0     # Radius for vertical corner fillets
hole_diameter = 6.0     # Diameter of the mounting holes

# --- Modeling ---

# 1. Create Base Block
# We start with a full rectangular block centered at the origin.
# Centering facilitates symmetry and coordinate calculations.
base = cq.Workplane("XY").box(length, width, height)

# 2. Apply Fillets
# We fillet the vertical edges of the base block *before* cutting the step.
# This ensures the outer corners of the original block boundary are rounded,
# while the subsequent cut operation will create sharp corners at the step transition,
# exactly matching the geometry in the image.
result = base.edges("|Z").fillet(fillet_radius)

# 3. Create the Step (Cutout)
# We remove a rectangular section from the front-right corner to form the L-profile.
# The cutter needs to be positioned in the (+X, -Y) quadrant.
cut_width = width - narrow_width
cut_len = step_length

# Calculate center position for the cutter box relative to the global origin
x_pos = (length / 2) - (cut_len / 2)
y_pos = -(width / 2) + (cut_width / 2)

cutter = (
    cq.Workplane("XY")
    .box(cut_len, cut_width, height * 2)  # Height * 2 ensures a complete through-cut
    .translate((x_pos, y_pos, 0))
)

result = result.cut(cutter)

# 4. Create Holes
# Holes are located on the top face (>Z) and appear aligned along the centerline of the narrow section.

# Y-offset: Center of the remaining material on the back strip.
# The narrow section occupies the back of the part (+Y direction relative to our cut).
# Center Y is the midpoint between the back edge and the step edge.
hole_y_offset = (width / 2) - (narrow_width / 2)

# X-offsets: Centered within their respective block sections.
# Center of the wide section (Left side): Midpoint of X range [-length/2, length/2 - step_length]
x_center_wide = (-length/2 + (length/2 - step_length)) / 2

# Center of the narrow section (Right side): Midpoint of X range [length/2 - step_length, length/2]
x_center_narrow = ((length/2 - step_length) + length/2) / 2

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([
        (x_center_wide, hole_y_offset), 
        (x_center_narrow, hole_y_offset)
    ])
    .hole(hole_diameter)
)