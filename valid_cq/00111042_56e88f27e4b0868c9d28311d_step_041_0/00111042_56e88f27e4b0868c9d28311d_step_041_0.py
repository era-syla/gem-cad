import cadquery as cq

# Parametric dimensions for the model
total_height = 300.0  # Total length of the vertical bar
width = 6.0           # Width of the bar
thickness = 6.0       # Thickness of the bar
segment_height = 6.0  # Height of each visual segment (pitch)
groove_height = 0.5   # Vertical size of the cut separating segments

# 1. Create the base vertical rectangular bar centered at the origin
# The bar extends along the Z-axis
base = cq.Workplane("XY").box(width, thickness, total_height)

# 2. Define the cutting tool to create the segmented look
# We calculate the number of cuts needed based on the total height and segment height
num_cuts = int(total_height / segment_height)

# Generate a list of center points (x, y, z) for each cut
# We start from the bottom and move up by 'segment_height'
cut_points = []
for i in range(1, num_cuts):
    z_pos = -total_height / 2 + (i * segment_height)
    cut_points.append((0, 0, z_pos))

# Create a compound object of multiple cutting plates using pushPoints
# We make the cutter slightly larger in X and Y to ensure a clean cut through the bar
cutter = (
    cq.Workplane("XY")
    .pushPoints(cut_points)
    .box(width * 2.0, thickness * 2.0, groove_height)
)

# 3. Apply the cut to the base object to create the final segmented bar
result = base.cut(cutter)