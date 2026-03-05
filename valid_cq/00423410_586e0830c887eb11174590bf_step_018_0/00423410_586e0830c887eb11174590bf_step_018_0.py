import cadquery as cq

# -- Parametric Dimensions --
width = 120.0         # Overall width of the frame
height = 80.0         # Overall height of the frame
thickness = 6.0       # Thickness of the extrusion
frame_side = 10.0     # Width of the frame on left and right sides
frame_top = 10.0      # Width of the frame on the top edge
frame_bottom = 20.0   # Width of the frame on the bottom edge (thicker "chin")
corner_radius = 4.0   # Fillet radius for the outer corners

# -- Helper Calculations --
# Calculate the dimensions of the inner rectangular hole
hole_width = width - (2 * frame_side)
hole_height = height - (frame_top + frame_bottom)

# Calculate the vertical offset for the hole center.
# The base box is centered at (0,0).
# We shift the hole center to account for the difference between top and bottom frame widths.
# A thicker bottom frame pushes the hole center upwards (+Y).
y_offset = (frame_bottom - frame_top) / 2.0

# -- Geometry Generation --
result = (
    cq.Workplane("XY")
    # 1. Create the base solid block
    .box(width, height, thickness)
    
    # 2. Fillet the four outer corners (vertical edges relative to XY plane)
    .edges("|Z")
    .fillet(corner_radius)
    
    # 3. Create the rectangular cutout
    .faces(">Z")              # Select the top face
    .workplane()              # Create a workplane on the top face
    .center(0, y_offset)      # Shift the grid center for the hole
    .rect(hole_width, hole_height) # Draw the rectangle to be cut
    .cutBlind(-thickness)     # Cut through the material
)