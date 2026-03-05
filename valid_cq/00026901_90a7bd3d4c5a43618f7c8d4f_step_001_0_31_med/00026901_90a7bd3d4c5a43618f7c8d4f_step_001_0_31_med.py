import cadquery as cq

# Paperclip parameters
wire_dia = 1.0
d = 3.0  # Spacing between the straight wire segments

# X-coordinates of the four straight segments (from inner to outer)
x1 = 0.0
x2 = x1 + d
x3 = x2 + d
x4 = x3 + d

# Y-coordinates for the bends and ends
y_top_inner = 28.0
y_bottom = 0.0
y_top_outer = 32.0
y_start_inner = 10.0
y_end_outer = 8.0

# Create the 2D path of the paperclip
path = (
    cq.Workplane("XY")
    .moveTo(x3, y_start_inner)
    .lineTo(x3, y_top_inner)
    # Inner top bend
    .threePointArc(((x2 + x3) / 2.0, y_top_inner + (x3 - x2) / 2.0), (x2, y_top_inner))
    .lineTo(x2, y_bottom)
    # Bottom bend
    .threePointArc(((x1 + x2) / 2.0, y_bottom - (x2 - x1) / 2.0), (x1, y_bottom))
    .lineTo(x1, y_top_outer)
    # Outer top bend
    .threePointArc(((x1 + x4) / 2.0, y_top_outer + (x4 - x1) / 2.0), (x4, y_top_outer))
    .lineTo(x4, y_end_outer)
)

# Create the circular profile at the start of the path
# The plane is normal to the start direction (Y-axis)
profile = (
    cq.Workplane(cq.Plane(origin=(x3, y_start_inner, 0), normal=(0, 1, 0)))
    .circle(wire_dia / 2.0)
)

# Sweep the profile along the path to create the solid body
result = profile.sweep(path, isFrenet=True)