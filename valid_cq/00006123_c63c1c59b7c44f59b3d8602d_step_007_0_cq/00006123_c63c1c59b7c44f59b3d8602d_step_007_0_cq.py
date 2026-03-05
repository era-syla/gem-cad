import cadquery as cq

# Parametric dimensions
length = 100.0   # Total length of the bar
width = 20.0     # Total width of the bar
thickness = 5.0  # Thickness of the bar
fillet_radius = 2.0 # Radius for the rounded corners of the bar

# Hole parameters
rows = 2
cols = 10
hole_length = 6.0  # Length of the rectangular hole
hole_width = 4.0   # Width of the rectangular hole
hole_corner_radius = 1.0 # Fillet radius for the hole corners
hole_spacing_x = 9.0  # Center-to-center spacing along length
hole_spacing_y = 8.0  # Center-to-center spacing along width

# Calculate grid layout
start_x = -(cols - 1) * hole_spacing_x / 2
start_y = -(rows - 1) * hole_spacing_y / 2

# Create the base rectangular plate
base = cq.Workplane("XY").box(length, width, thickness)

# Apply fillets to the four vertical edges of the base
base = base.edges("|Z").fillet(fillet_radius)

# Define the shape of a single hole (rectangular with rounded corners)
def create_hole_profile(loc):
    return (
        cq.Workplane("XY")
        .rect(hole_length, hole_width)
        .extrude(thickness)
        .edges("|Z")
        .fillet(hole_corner_radius)
        .val()
        .located(loc)
    )

# Create a list of locations for the holes
locations = []
for r in range(rows):
    y = start_y + r * hole_spacing_y
    for c in range(cols):
        x = start_x + c * hole_spacing_x
        locations.append(cq.Location(cq.Vector(x, y, 0)))

# Create the cutting tool by combining hole shapes at all locations
# We create a sketch profile and extrude it to cut
holes = (
    cq.Workplane("XY")
    .pushPoints([(loc.toTuple()[0][0], loc.toTuple()[0][1]) for loc in locations])
    .rect(hole_length, hole_width)
    .extrude(thickness)
    .edges("|Z")
    .fillet(hole_corner_radius)
)

# Cut the holes from the base
result = base.cut(holes)