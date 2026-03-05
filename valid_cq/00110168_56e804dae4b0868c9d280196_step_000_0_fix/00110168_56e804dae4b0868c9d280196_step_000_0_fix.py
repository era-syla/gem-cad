import cadquery as cq

# Parameters
left_radius = 2.0
left_length = 50.0
block_width = 8.0
block_height = 8.0
block_thickness = 5.0
rail_length = 70.0
rail_width = 1.5
rail_thickness = 1.5
rail_spacing = 4.0

# Build the part
result = (
    cq.Workplane("XY")
    # Left cylindrical rod
    .circle(left_radius).extrude(left_length)
    # Central square block
    .faces(">Z").workplane()
    .rect(block_width, block_height).extrude(block_thickness)
    # Two parallel rails
    .faces(">Z").workplane()
    .pushPoints([(-(rail_width + rail_spacing)/2, 0), ((rail_width + rail_spacing)/2, 0)])
    .rect(rail_width, rail_thickness).extrude(rail_length)
)