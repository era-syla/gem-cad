import cadquery as cq

# Parametric dimensions based on the provided image
total_height = 250.0   # Total length of the bar
width = 8.0            # Width of the bar cross-section
thickness = 8.0        # Thickness of the bar cross-section
notch_height = 20.0    # Vertical length of the notch at the top
notch_depth = 4.0      # Depth of the notch (removing approx. half the thickness)

# Create the main vertical bar
# Centered at origin, extending from -total_height/2 to +total_height/2 in Z
result = cq.Workplane("XY").box(width, thickness, total_height)

# Calculate positions for the cutout
# The cut is located at the top face (+Z) and cuts into one side (+Y)
# Z-center of the cut volume: (Top Z) - (Half of notch height)
cut_z_center = (total_height / 2.0) - (notch_height / 2.0)

# Y-center of the cut volume: (Face Y) - (Half of notch depth)
# The face is at thickness/2, we move inwards by notch_depth/2
cut_y_center = (thickness / 2.0) - (notch_depth / 2.0)

# Create the cutting volume (a box representing the material to remove)
# We position a workplane at the calculated Z and Y offsets
cutter = (
    cq.Workplane("XY")
    .workplane(offset=cut_z_center)
    .center(0, cut_y_center)
    .box(width, notch_depth, notch_height)
)

# Subtract the cutter from the main bar to create the notched end
result = result.cut(cutter)