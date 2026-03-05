import cadquery as cq

# -----------------------------------------------------------------------------
# Parameters
# -----------------------------------------------------------------------------
text_string = "UHTRED"
font_size = 12.0
thickness = 3.0       # Extrusion depth for both text and base
bar_height = 3.5      # Height (y-direction) of the connecting bottom bar
hole_diameter = 2.5   # Diameter of the keyring hole
margin_left = 2.0     # Material extending to the left of the text
margin_right = 6.5    # Material extending to the right (includes hole area)

# -----------------------------------------------------------------------------
# Model Generation
# -----------------------------------------------------------------------------

# 1. Generate the Text Solid
# text() creates a solid object centered at (0,0) by default
text_obj = cq.Workplane("XY").text(text_string, font_size, thickness)

# 2. Analyze Geometry
# Get bounding box to determine sizing and positioning of the base bar
bb = text_obj.val().BoundingBox()
t_xmin = bb.xmin
t_xmax = bb.xmax
t_ymin = bb.ymin

# 3. Create the Base Bar
# The bar runs along the bottom of the letters to connect them.
# It is positioned starting from the bottom of the text (t_ymin).

# Calculate center positions for the bar
bar_y_center = t_ymin + (bar_height / 2.0)
bar_x_start = t_xmin - margin_left
bar_x_end = t_xmax + margin_right
bar_length = bar_x_end - bar_x_start
bar_x_center = bar_x_start + (bar_length / 2.0)

# Create rectangular solid
base_bar = (
    cq.Workplane("XY")
    .moveTo(bar_x_center, bar_y_center)
    .rect(bar_length, bar_height)
    .extrude(thickness)
)

# Fillet the vertical edges to create rounded ends (stadium/pill shape)
# Radius is effectively half the height
fillet_radius = (bar_height / 2.0) - 0.01
base_bar = base_bar.edges("|Z").fillet(fillet_radius)

# 4. Create the Keyring Hole
# The hole is located on the right extension tab.
# We align it with the center of the right-side rounded end.
hole_x = bar_x_end - (bar_height / 2.0)
hole_y = bar_y_center

base_bar_with_hole = (
    base_bar.faces(">Z").workplane()
    .moveTo(hole_x, hole_y)
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)

# 5. Final Union
# Combine the text letters with the base bar
result = text_obj.union(base_bar_with_hole)