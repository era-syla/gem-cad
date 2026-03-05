import cadquery as cq

# Parametric dimensions
length = 100.0
height = 40.0
thickness = 4.0
gap = 12.0
web_length = 15.0
web_height = 25.0
corner_radius = 3.0
fillet_radius = 1.5
overlap = 1.0 # Used to ensure robust boolean union

# Create front plate
front_plate = (
    cq.Workplane("XY")
    .workplane(offset=gap / 2.0)
    .rect(length, height)
    .extrude(thickness)
    .edges("|Z")
    .fillet(corner_radius)
    .faces(">Z")
    .edges()
    .fillet(fillet_radius)
)

# Create back plate
back_plate = (
    cq.Workplane("XY")
    .workplane(offset=-gap / 2.0)
    .rect(length, height)
    .extrude(-thickness)
    .edges("|Z")
    .fillet(corner_radius)
    .faces("<Z")
    .edges()
    .fillet(fillet_radius)
)

# Create central web (slightly extending into the plates to guarantee a clean union)
web = (
    cq.Workplane("XY")
    .workplane(offset=-(gap / 2.0) - overlap)
    .rect(web_length, web_height)
    .extrude(gap + 2.0 * overlap)
)

# Combine parts into the final solid
result = front_plate.union(back_plate).union(web)