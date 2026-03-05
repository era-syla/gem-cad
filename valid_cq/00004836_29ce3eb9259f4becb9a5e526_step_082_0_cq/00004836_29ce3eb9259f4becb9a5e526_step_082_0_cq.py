import cadquery as cq

# --- Parametric Dimensions ---
length = 500.0       # Total length of the strip
width = 25.0         # Width of the strip
thickness = 3.0      # Thickness of the strip
num_holes = 10       # Number of holes
hole_diameter = 4.0  # Diameter of the through holes
csk_diameter = 8.0   # Diameter of the countersink
csk_angle = 90.0     # Countersink angle in degrees

# Calculate spacing
# Spacing between hole centers. 
# We assume equal spacing and some margin at the ends.
# Let's say the first and last holes are spaced by 'spacing' from the ends as well, 
# or just evenly distributed. Let's assume evenly distributed along the length.
# If there are N holes, there are N+1 gaps if we include ends, or N-1 intervals.
# A common pattern is start_offset + (n * pitch).
# Let's try to center the array of holes.
hole_pitch = length / (num_holes + 1) # Equal spacing from ends and between holes

# --- Modeling ---

# 1. Create the base rectangular strip
strip = cq.Workplane("XY").box(width, length, thickness)

# 2. Create the list of points for the holes
# The strip is centered at (0,0,0). The length is along Y.
# Y ranges from -length/2 to +length/2.
hole_points = []
start_y = -length/2 + hole_pitch

for i in range(num_holes):
    y_pos = start_y + (i * hole_pitch)
    hole_points.append((0, y_pos))

# 3. Cut the holes
# We select the top face (Z positive) to drill through.
result = (
    strip
    .faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .cskHole(hole_diameter, csk_diameter, csk_angle, depth=None) # cskHole creates a countersunk hole
)

# If simple holes are preferred without countersink, use:
# result = strip.faces(">Z").workplane().pushPoints(hole_points).hole(hole_diameter)

# Export or visualization would happen externally, 'result' is the required variable.