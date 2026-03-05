import cadquery as cq

# Parametric dimensions for the model
bar_length = 200.0
bar_width = 6.0
bar_height = 6.0
tab_length = 12.0
tab_protrusion = 6.0

# Create the main elongated bar centered at the origin
# Aligned along the X-axis
result = cq.Workplane("XY").box(bar_length, bar_width, bar_height)

# Create the tab feature at one end of the bar
# 1. Select the side face (-Y direction)
# 2. Create a new workplane on that face
# 3. Move the center to the end of the bar (-X end), adjusting for the tab's length
# 4. Draw the rectangle profile of the tab (length along X, height along Z)
# 5. Extrude the tab outwards from the bar
result = (
    result.faces("<Y")
    .workplane()
    .center(-bar_length / 2 + tab_length / 2, 0)
    .rect(tab_length, bar_height)
    .extrude(tab_protrusion)
)