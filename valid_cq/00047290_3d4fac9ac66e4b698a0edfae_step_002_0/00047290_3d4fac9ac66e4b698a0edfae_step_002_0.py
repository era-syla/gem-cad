import cadquery as cq

# Parameters defining the geometry
width = 120.0        # Overall width of the frame
height = 100.0       # Overall height of the frame
thickness = 5.0      # Thickness of the plate
frame_width = 10.0   # Width of the borders and vertical dividers (mullions)
num_panes = 3        # Number of window panes

# Calculate internal dimensions derived from parameters
# Total width occupied by vertical frame elements (left, right, and internal dividers)
total_vertical_frame = (num_panes + 1) * frame_width

# Width of a single pane
pane_width = (width - total_vertical_frame) / num_panes

# Height of a pane (total height minus top and bottom borders)
pane_height = height - (2 * frame_width)

# Center-to-center spacing for the panes
pane_spacing = pane_width + frame_width

# Create the 3D Model
# 1. Create the base solid plate
result = cq.Workplane("XY").box(width, height, thickness)

# 2. Create the cutouts
# Select the top face, create a grid of points using rarray, 
# sketch rectangles at those points, and cut through the material.
result = (
    result.faces(">Z")
    .workplane()
    .rarray(
        xSpacing=pane_spacing, 
        ySpacing=1,            # Y spacing is irrelevant for a 1-row array
        xCount=num_panes, 
        yCount=1
    )
    .rect(pane_width, pane_height)
    .cutThruAll()
)