import cadquery as cq

# Parameters
outer_radius = 50.0  # Distance from center to outer vertex
thickness = 10.0     # Total thickness of the plate
fillet_radius = 5.0  # Radius of the outer corners
center_hole_dia = 25.0 # Diameter of the central through-hole
bolt_circle_dia = 75.0 # Diameter of the circle where bolt holes are placed (approx)
bolt_hole_dia = 4.0    # Diameter of the small bolt holes
recess_depth = 5.0     # Depth of the hexagonal pocket
recess_size_factor = 0.65 # Ratio of inner hex size to outer hex size

# Derived parameters
outer_hex_side = outer_radius  # For a regular hexagon, side length equals radius
inner_radius = outer_radius * recess_size_factor

# 1. Base Hexagon
# Create the main hexagonal body
base = (
    cq.Workplane("XY")
    .polygon(6, outer_radius * 2) # polygon takes diameter (point-to-point)
    .extrude(thickness)
)

# 2. Corner Fillets
# Select the vertical edges of the hexagon and fillet them
base = base.edges("|Z").fillet(fillet_radius)

# 3. Hexagonal Recess
# Create a twisted/rotated hexagonal pocket.
# Looking at the image, the inner hex pocket is rotated relative to the outer one.
# The vertices of the inner hex seem to touch the midpoints or sides of the outer hex structure,
# creating that triangular "shelf" look. 
# Let's create a hexagon for the pocket.
recess = (
    base.faces(">Z")
    .workplane()
    .transformed(rotate=(0, 0, 30)) # Rotate 30 degrees to align vertices with flats
    .polygon(6, inner_radius * 2)
    .cutBlind(-recess_depth)
)

# 4. Central Hole
# Cut the through-hole in the center
with_center_hole = (
    recess.faces(">Z")
    .workplane()
    .circle(center_hole_dia / 2)
    .cutThruAll()
)

# 5. Bolt Holes
# There are 6 small holes on the raised rim.
# They are located near the outer corners.
# Since we rotated the inner pocket, let's look at the outer rim alignment.
# The holes are aligned with the vertices of the outer hexagon.
result = (
    with_center_hole.faces(">Z")
    .workplane()
    .polarArray(outer_radius * 0.8, 0, 360, 6) # Radius for hole placement
    .circle(bolt_hole_dia / 2)
    .cutBlind(-thickness) # Cut through
)