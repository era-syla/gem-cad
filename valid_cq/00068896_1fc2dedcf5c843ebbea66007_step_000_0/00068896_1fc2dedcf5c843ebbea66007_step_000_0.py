import cadquery as cq

# Parametric Dimensions
# Main housing body dimensions
body_diameter = 28.0
body_length = 14.0
back_fillet_radius = 8.0  # Creates the rounded domed back

# Shaft dimensions
shaft_1_diameter = 13.0
shaft_1_length = 15.0
shaft_2_diameter = 9.0
shaft_2_length = 11.0

# Locking tabs dimensions
tab_width = 5.0       # Tangential width
tab_protrusion = 2.5  # Radial height sticking out
tab_axial_len = 5.0   # Length along the body
tab_overlap = 1.0     # Amount the tab sinks into the body for a solid union

# --- Modeling ---

# 1. Create the main housing body
# Oriented along the Z-axis, starting from Z=0
main_body = cq.Workplane("XY").circle(body_diameter / 2.0).extrude(body_length)

# Apply fillet to the rear edge to create the domed shape
# Selecting edges at Z=0 (<Z)
main_body = main_body.edges("<Z").fillet(back_fillet_radius)

# 2. Create the Shafts
# Shaft Section 1: Extrudes from the front face of the main body
shaft_1 = (
    cq.Workplane("XY")
    .workplane(offset=body_length)
    .circle(shaft_1_diameter / 2.0)
    .extrude(shaft_1_length)
)

# Shaft Section 2: Extrudes from the end of Shaft 1
shaft_2 = (
    cq.Workplane("XY")
    .workplane(offset=body_length + shaft_1_length)
    .circle(shaft_2_diameter / 2.0)
    .extrude(shaft_2_length)
)

# 3. Create the Side Tabs
# We calculate the position and size of the rectangle to form the tabs.
# The tabs are positioned on the X-axis on opposite sides.
rect_radial_width = tab_protrusion + tab_overlap
rect_center_offset = (body_diameter / 2.0) - tab_overlap + (rect_radial_width / 2.0)

# Create tabs by starting at the shoulder face and extruding backwards
tabs = (
    cq.Workplane("XY")
    .workplane(offset=body_length)
    .pushPoints([(rect_center_offset, 0), (-rect_center_offset, 0)])
    .rect(rect_radial_width, tab_width)
    .extrude(-tab_axial_len)
)

# 4. Combine all components into the final result
result = main_body.union(shaft_1).union(shaft_2).union(tabs)