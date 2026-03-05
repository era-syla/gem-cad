import cadquery as cq

# Parameter definitions for the model geometry
# Dimensions are estimated based on visual proportions from the image
base_diameter = 14.0
base_height = 8.0

shaft_diameter = 8.0
shaft_length = 16.0

hex_section_length = 24.0
# The hex section appears to be milled from the shaft stock, 
# so the distance across corners equals the shaft diameter.
hex_across_corners = shaft_diameter

pin_diameter = 4.0
pin_length = 6.0

# Construct the solid geometry
result = (
    cq.Workplane("XY")
    # 1. Create the bottom cylindrical base
    .circle(base_diameter / 2.0)
    .extrude(base_height)
    
    # 2. Create the middle cylindrical shaft section
    .faces(">Z").workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
    
    # 3. Create the hexagonal section
    # Use a 6-sided polygon where the diameter represents the circle inscribing the polygon (across corners)
    .faces(">Z").workplane()
    .polygon(6, hex_across_corners)
    .extrude(hex_section_length)
    
    # 4. Create the top cylindrical pin
    .faces(">Z").workplane()
    .circle(pin_diameter / 2.0)
    .extrude(pin_length)
)