import cadquery as cq

# 1. Define parametric dimensions for the model
length = 100.0        # Total length of the part
width_end = 70.0      # Width at the straight ends
width_waist = 30.0    # Narrowest width at the center
thickness = 8.0       # Thickness of the plate
tab_radius = 5.0      # Radius of the connection tabs

# Calculated coordinates
x_pos = length / 2.0
x_neg = -length / 2.0
y_pos = width_end / 2.0
y_neg = -width_end / 2.0
y_waist_pos = width_waist / 2.0
y_waist_neg = -width_waist / 2.0

# 2. Create the main plate body
# The shape is defined by straight vertical edges at the ends and concave arcs on top/bottom
plate = (
    cq.Workplane("XY")
    .moveTo(x_pos, y_neg)                          # Start at Bottom-Right corner
    .lineTo(x_pos, y_pos)                          # Line to Top-Right corner
    .threePointArc((0, y_waist_pos), (x_neg, y_pos)) # Concave arc to Top-Left
    .lineTo(x_neg, y_neg)                          # Line to Bottom-Left corner
    .threePointArc((0, y_waist_neg), (x_pos, y_neg)) # Concave arc to Bottom-Right
    .close()
    .extrude(thickness)
)

# 3. Create the circular tabs
# Tabs are located at the 4 corners and the middle of the two straight edges
tab_locations = [
    (x_pos, y_pos),   # Top-Right Corner
    (x_pos, y_neg),   # Bottom-Right Corner
    (x_neg, y_pos),   # Top-Left Corner
    (x_neg, y_neg),   # Bottom-Left Corner
    (x_pos, 0),       # Right Edge Center
    (x_neg, 0)        # Left Edge Center
]

tabs = (
    cq.Workplane("XY")
    .pushPoints(tab_locations)
    .circle(tab_radius)
    .extrude(thickness)
)

# 4. Combine the plate and tabs into the final geometry
result = plate.union(tabs)