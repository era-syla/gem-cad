import cadquery as cq

# Parametric dimensions
length = 120.0
width = 40.0
height = 30.0
tab_length = 20.0
tab_height = 6.0
fillet_radius = 12.0

# Define profile points for the XZ plane sketch
p_start = (-length / 2, 0)
p1 = (length / 2, 0)
p2 = (length / 2, tab_height)
p3 = (length / 2 - tab_length + fillet_radius, tab_height)
p4 = (length / 2 - tab_length, tab_height + fillet_radius)
p5 = (length / 2 - tab_length, height)
p6 = (-length / 2 + tab_length, height)
p7 = (-length / 2 + tab_length, tab_height + fillet_radius)
p8 = (-length / 2 + tab_length - fillet_radius, tab_height)
p9 = (-length / 2, tab_height)

# Create the 3D model
result = (
    cq.Workplane("XZ")
    .moveTo(*p_start)
    .lineTo(*p1)
    .lineTo(*p2)
    .lineTo(*p3)
    # Negative radius is used for a clockwise arc
    .radiusArc(p4, -fillet_radius)
    .lineTo(*p5)
    .lineTo(*p6)
    .lineTo(*p7)
    .radiusArc(p8, -fillet_radius)
    .lineTo(*p9)
    .close()
    .extrude(width / 2, both=True)
)