import cadquery as cq

# Parametric dimensions
length = 200.0       # Total length of the bar
width = 20.0         # Width of the bar
height = 10.0        # Height of the main body
end_step_height = 5.0 # Height of the stepped down sections at ends
end_step_length = 20.0 # Length of the stepped down sections
hole_diameter = 4.0  # Diameter of the mounting holes
tab_width = 3.0      # Width of the small alignment tabs
tab_height = 2.0     # Height of the tabs above the step surface
tab_length = 3.0     # Length (depth) of the tabs

# Calculated dimensions
# The step surface is lower than the main height
step_z_level = height - end_step_height

# 1. Create the main rectangular block
base = cq.Workplane("XY").box(length, width, height)

# 2. Create the cutouts for the stepped ends
# We will cut away the top material at both ends
# Define the cutting tool
cut_tool = (
    cq.Workplane("XY")
    .workplane(offset=height - end_step_height)
    .rect(end_step_length, width)
    .extrude(end_step_height)
)

# Position and cut on left side
left_cut = cut_tool.translate((-length/2 + end_step_length/2, 0, 0))
# Position and cut on right side
right_cut = cut_tool.translate((length/2 - end_step_length/2, 0, 0))

# Apply cuts
result = base.cut(left_cut).cut(right_cut)

# 3. Add mounting holes
# Position: centered on the stepped surfaces
hole_x_offset = length/2 - end_step_length/2
result = (
    result.faces(">Z").workplane()
    .pushPoints([(-hole_x_offset, 0), (hole_x_offset, 0)])
    .hole(hole_diameter)
)

# 4. Add the alignment tabs/teeth
# There are two small tabs on each end, positioned at the edge of the original block width
# The tabs sit on the stepped surface

# Define a single tab shape
tab = (
    cq.Workplane("XY")
    .rect(tab_length, tab_width)
    .extrude(tab_height)
)

# Coordinates for tabs
# X: Inner edge of the step area. The step starts at +/- (length/2 - end_step_length).
#    The image shows the tabs slightly offset or at the shoulder. Let's place them against the shoulder.
#    Wait, looking closer at the image, the tabs are at the very ends of the bar, on the step surface.
#    Let's re-examine.
#    The tabs are on the side edges of the step.
#    X position: Center of the step area or aligned with hole? Let's align with hole X for simplicity or slightly offset.
#    Looking at the image, the tabs are aligned with the hole center along X, on the edges of Y.

tab_x_pos = length/2 - end_step_length/2
tab_y_pos = width/2 - tab_width/2
tab_z_pos = height - end_step_height

# Create tabs for all 4 corners
tabs = (
    cq.Workplane("XY")
    .workplane(offset=tab_z_pos)
    .pushPoints([
        (-tab_x_pos, -tab_y_pos), (-tab_x_pos, tab_y_pos), # Left end
        (tab_x_pos, -tab_y_pos), (tab_x_pos, tab_y_pos)    # Right end
    ])
    .rect(tab_length, tab_width)
    .extrude(tab_height)
)

# Combine the base with the tabs
result = result.union(tabs)

# Export the result if needed (optional context)
# cq.exporters.export(result, "part.step")