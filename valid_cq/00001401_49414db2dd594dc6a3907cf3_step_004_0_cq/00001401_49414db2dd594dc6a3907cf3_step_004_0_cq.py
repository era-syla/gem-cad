import cadquery as cq

# Parametric dimensions
plate_length = 200.0
plate_width = 140.0
plate_thickness = 5.0
hole_diameter = 6.0

# Hole pattern parameters
long_edge_margin = 15.0  # Distance from the long edge
short_edge_margin = 15.0 # Distance from the short edge

# Calculate positions
# We need holes along the perimeter. Let's analyze the image pattern.
# There appear to be 4 holes along each long side and likely 3 along the short sides (including corners).
# Looking at the image:
# Left short edge: 3 holes
# Right short edge: 3 holes (implied)
# Front long edge: 4 holes (including corners)
# Back long edge: 4 holes (including corners)
# Total: 3 on left + 3 on right + 2 in middle front + 2 in middle back = 10 holes? 
# Or simply a grid of points on the perimeter?
# Let's count them carefully.
# Visible front-left short edge has holes at corner, middle, corner.
# Visible front-right long edge seems to have holes at corner, middle-ish, middle-ish, corner.
# It looks like:
# - Short edges have a hole in the middle.
# - Long edges have two intermediate holes.
# This suggests:
# x-coordinates (along length): -L/2 + margin, -L/6?, +L/6?, +L/2 - margin
# y-coordinates (along width): -W/2 + margin, 0, +W/2 - margin
#
# Let's verify with a simpler interpretation:
# A set of points along the long edges and short edges.
# Long edge spacing: evenly spaced.
# Short edge spacing: evenly spaced.

# Let's define the hole centers
# Corner holes (4)
x_outer = plate_length / 2 - short_edge_margin
y_outer = plate_width / 2 - long_edge_margin

# Intermediate holes along long edges (Let's assume 2 intermediate holes, creating 3 intervals)
# x coords: -x_outer, -x_outer/3, +x_outer/3, +x_outer
# Intermediate holes along short edges (Let's assume 1 intermediate hole, creating 2 intervals)
# y coords: 0

pts = []

# Top and Bottom rows (Long edges)
# Assuming 4 holes per long edge based on visual spacing
# x positions: roughly -85, -28.3, 28.3, 85 (if length 200)
num_holes_long = 4
step_x = (2 * x_outer) / (num_holes_long - 1)

for i in range(num_holes_long):
    x_pos = -x_outer + i * step_x
    pts.append((x_pos, y_outer))  # Back edge
    pts.append((x_pos, -y_outer)) # Front edge

# Side holes (Short edges)
# We already have the corners from the loop above.
# We just need the middle ones on the short edges.
# It looks like there is 1 hole in the middle of the short edge.
pts.append((-x_outer, 0)) # Left edge middle
pts.append((x_outer, 0))  # Right edge middle

# Create the plate
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints(pts)
    .hole(hole_diameter)
)