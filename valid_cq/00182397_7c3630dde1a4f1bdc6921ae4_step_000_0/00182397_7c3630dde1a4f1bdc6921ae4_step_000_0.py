import cadquery as cq

# Parametric dimensions
# Main plate dimensions
main_length = 50.0
main_width = 30.0
main_thickness = 2.0

# Small tab dimensions
tab_length = 15.0
tab_width = 12.0
tab_thickness = 2.0

# Create the main body (large plate)
# Centered at origin
main_body = cq.Workplane("XY").box(main_length, main_width, main_thickness)

# Calculate offsets to position the tab
# X offset: Places the tab adjacent to the main plate along the X axis
x_offset = (main_length / 2.0) + (tab_length / 2.0)

# Z offset: Lowers the tab so its top face is flush with the bottom face of the main body
# (Assuming center-based creation, the shift is sum of half-thicknesses)
z_offset = -(main_thickness / 2.0) - (tab_thickness / 2.0)

# Create the tab and position it
tab = (
    cq.Workplane("XY")
    .box(tab_length, tab_width, tab_thickness)
    .translate((x_offset, 0, z_offset))
)

# Combine the parts into a single solid
result = main_body.union(tab)