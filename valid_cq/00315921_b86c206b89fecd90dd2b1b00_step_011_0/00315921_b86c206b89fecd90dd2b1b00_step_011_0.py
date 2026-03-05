import cadquery as cq

# --- Geometric Parameters ---
length = 150.0          # Total length of the part
width = 25.0            # Width of the part
thickness = 10.0        # Thickness (height) of the part
fillet_radius = 5.0     # Radius of the vertical corner fillets

# Hole parameters
hole_diameter = 6.0     # Diameter of the through holes
hole_spacing = 15.0     # Distance between the two holes in a pair
end_margin = 10.0       # Distance from the end of the bar to the center of the first hole

# Groove parameters
groove_radius = 4.0     # Radius of the semi-circular grooves
groove_pitch = 14.0     # Distance between groove centers
num_grooves = 4         # Total number of grooves

# --- Model Construction ---

# 1. Create the base rectangular block
# The box is centered at (0,0,0), so Z ranges from -thickness/2 to thickness/2
base = cq.Workplane("XY").box(length, width, thickness)

# 2. Fillet the vertical edges (parallel to Z axis)
base = base.edges("|Z").fillet(fillet_radius)

# 3. Create the mounting holes
# Calculate X coordinates for the holes. They are symmetric about the center.
x_outer = length / 2.0 - end_margin
x_inner = x_outer - hole_spacing

# Define the points for the 4 holes
hole_locations = [
    (-x_outer, 0), (-x_inner, 0),
    (x_inner, 0), (x_outer, 0)
]

# Select the top face and drill the holes
result = base.faces(">Z").workplane().pushPoints(hole_locations).hole(hole_diameter)

# 4. Create the transverse grooves
# We will create a "cutter" object consisting of cylinders and subtract it from the main body.
# The grooves are centered on the top face (z = thickness/2) and run along the Y axis (width).

groove_centers_xz = []
for i in range(num_grooves):
    # Calculate x position centered around the origin
    # Formula centers the array of grooves: e.g., for 4 grooves at -1.5p, -0.5p, 0.5p, 1.5p
    x_pos = (i - (num_grooves - 1) / 2.0) * groove_pitch
    z_pos = thickness / 2.0
    groove_centers_xz.append((x_pos, z_pos))

# Sketch the groove profiles on the XZ plane (side view)
# We extrude these circles along Y (both directions) to span the full width of the part
cutter = (
    cq.Workplane("XZ")
    .pushPoints(groove_centers_xz)
    .circle(groove_radius)
    .extrude(width, both=True)  # Extrude far enough to cut through the entire width
)

# Subtract the cutter geometry from the main part
result = result.cut(cutter)