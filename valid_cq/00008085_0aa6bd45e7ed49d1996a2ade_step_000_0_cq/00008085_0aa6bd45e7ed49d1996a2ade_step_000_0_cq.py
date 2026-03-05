import cadquery as cq

# Parametric dimensions
rail_length = 500.0
rail_width = 12.0
rail_height = 8.0
groove_width = 4.0
groove_depth = 3.0

carriage_length = 30.0
carriage_width = 20.0
carriage_height = 15.0

# Create the main rail profile
# The rail looks like a rectangular bar with a groove running down the top
rail_profile = (
    cq.Sketch()
    .rect(rail_width, rail_height)
    .push([(0, rail_height/2)])
    .rect(groove_width, groove_depth * 2, mode='s') # Subtract groove
    .clean()
)

# Extrude the rail
rail = (
    cq.Workplane("XY")
    .placeSketch(rail_profile)
    .extrude(rail_length)
)

# Create the carriage/block
# The carriage sits on the rail, roughly in the middle
carriage_body = (
    cq.Workplane("XY")
    .rect(carriage_width, carriage_height)
    .extrude(carriage_length)
    .translate((0, (carriage_height/2) + (rail_height/2) - 1.0, rail_length/2 - carriage_length/2))
)

# Create a cutout in the carriage to fit over the rail
carriage_cutout_profile = (
    cq.Sketch()
    .rect(rail_width + 0.5, rail_height + 0.5) # Slight clearance
)

carriage_cutout = (
    cq.Workplane("XY")
    .placeSketch(carriage_cutout_profile)
    .extrude(carriage_length + 2) # Extra length for clean cut
    .translate((0, 0, rail_length/2 - carriage_length/2 - 1))
)

# Apply the cut to the carriage
carriage = carriage_body.cut(carriage_cutout)

# Detail: Mounting holes on the end of the rail (visible in the image on the right)
hole_diameter = 2.5
hole_spacing = 6.0
end_detail_location = rail_length - 5.0

rail = (
    rail.faces(">Z")
    .workplane()
    .pushPoints([(0, end_detail_location), (0, end_detail_location - 10)])
    .hole(hole_diameter, depth=rail_height)
)

# Detail: Slot or feature on the rail side
side_slot = (
    cq.Workplane("YZ")
    .rect(rail_height/2, rail_length)
    .extrude(1.0) # Shallow cut
    .translate((rail_width/2, rail_height/2, rail_length/2))
)
# Note: For simplicity, keeping the main rail shape clean as interpreted from the low-res image, 
# but adding the carriage to the assembly.

# Combine the parts
result = rail.union(carriage)

# Optional: Add fillets to the carriage for a more realistic look
result = result.edges("|Z").fillet(0.5)