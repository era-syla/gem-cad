import cadquery as cq

# Model Parameters
length = 100.0        # Total length of the plate
width = 60.0          # Total width of the plate at the ends
thickness = 3.0       # Thickness of the plate
notch_len = 60.0      # Length of the recessed section in the middle
notch_depth = 2.5     # Depth of the recess cut into the sides

# Create the base plate centered at the origin
base = cq.Workplane("XY").box(length, width, thickness)

# Create a cutting tool for the side notches
# The height of the box is notch_depth*2 to ensure it cuts through the edge
# when centered on the edge line
notch_tool = cq.Workplane("XY").box(notch_len, notch_depth * 2, thickness)

# Apply the cuts to both long edges of the plate
result = (
    base
    .cut(notch_tool.translate((0, width / 2, 0)))   # Cut the 'back' edge
    .cut(notch_tool.translate((0, -width / 2, 0)))  # Cut the 'front' edge
)