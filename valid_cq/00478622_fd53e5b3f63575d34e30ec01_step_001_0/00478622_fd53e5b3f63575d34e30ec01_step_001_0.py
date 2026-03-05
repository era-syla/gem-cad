import cadquery as cq

# Geometric Parameters
plate_length = 90.0
plate_width = 35.0
plate_thickness = 4.0
tab_width = 10.0
tab_extension = 5.0

# 1. Create the main rectangular body
# Centered at the origin by default
main_body = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Create the tabs
# We create a single long, narrow box that intersects the main body
# Length includes the main body length plus the extension on both ends
total_tab_length = plate_length + (2 * tab_extension)
tabs = cq.Workplane("XY").box(total_tab_length, tab_width, plate_thickness)

# 3. Combine the geometries
result = main_body.union(tabs)