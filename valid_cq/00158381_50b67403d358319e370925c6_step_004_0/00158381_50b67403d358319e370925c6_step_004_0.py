import cadquery as cq

# -- Geometric Parameters --
length = 400.0        # Total length of the panel
width = 220.0         # Total width of the panel
thickness = 6.0       # Thickness of the plate
chamfer_size = 1.5    # Size of the edge chamfer

# -- Hole Parameters --
hole_dia = 5.0        # Through-hole diameter
csk_dia = 10.0        # Countersink head diameter
csk_angle = 90.0      # Countersink angle
hole_margin = 15.0    # Offset from the edge to the hole center

# -- Model Generation --

# 1. Create the base rectangular plate centered on the XY plane
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Apply a chamfer to the top perimeter edges
# We select the face with the highest Z value, then select its boundary edges
result = result.faces(">Z").edges().chamfer(chamfer_size)

# 3. Create the mounting holes
# Calculate coordinates for 6 holes: 
# 3 along the X-axis (Left, Center, Right) and 2 along the Y-axis (Front, Back)
x_coords = [-(length / 2 - hole_margin), 0, (length / 2 - hole_margin)]
y_coords = [-(width / 2 - hole_margin), (width / 2 - hole_margin)]

# Generate the list of (x, y) points
hole_locations = [(x, y) for x in x_coords for y in y_coords]

# Drill countersunk holes at the defined locations starting from the top face
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .cskHole(hole_dia, csk_dia, csk_angle)
)