import cadquery as cq

# Parametric definitions
total_length = 150.0  # Total length of the object
rod_diameter = 5.0    # Diameter of the cylindrical shaft
head_height = 4.0     # Thickness of the hexagonal head
head_width = 8.0      # Distance across flats for the hexagonal head

# Create the hexagonal head
# We use polygon with 6 sides to create a hexagon
head = (
    cq.Workplane("XY")
    .polygon(nSides=6, diameter=head_width / 0.866025) # diameter is circumscribed, width is inscribed (flat-to-flat)
    .extrude(head_height)
)

# Create the cylindrical shaft attached to the head
shaft = (
    cq.Workplane("XY")
    .circle(rod_diameter / 2.0)
    .extrude(total_length)
)

# Combine the head and the shaft.
# Since both start at Z=0 and extrude in the positive Z direction, 
# we need to move the shaft or just extrude it from the face of the head.
# A simpler approach for valid geometry union is to create them separately and union them,
# or extrude the shaft from the top face of the head.

# Let's recreate using a single Workplane flow for cleaner parametric history
result = (
    cq.Workplane("XY")
    # Step 1: Create the Hex Head
    .polygon(nSides=6, diameter=head_width / (3**0.5 / 2)) # converting flat-to-flat to circumcircle diameter
    .extrude(head_height)
    # Step 2: Select the top face of the hex head
    .faces(">Z")
    .workplane()
    # Step 3: Create the cylindrical shaft
    .circle(rod_diameter / 2.0)
    .extrude(total_length - head_height)
)

# Alternative simpler method (uncomment to test if preferred, but the above is more robust)
# head = cq.Workplane("XY").polygon(6, head_width / 0.866).extrude(head_height)
# shaft = cq.Workplane("XY").workplane(offset=head_height).circle(rod_diameter/2).extrude(total_length - head_height)
# result = head.union(shaft)