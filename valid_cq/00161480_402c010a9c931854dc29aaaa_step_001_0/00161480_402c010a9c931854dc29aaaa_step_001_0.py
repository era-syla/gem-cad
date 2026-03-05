import cadquery as cq

# Parametric dimensions
total_height = 100.0
hex_thickness = 6.0
hex_circum_diameter = 24.0  # Diameter of the circle circumscribing the hexagon
shaft_diameter = 16.0

# Calculated dimension
shaft_length = total_height - (2 * hex_thickness)

# Generate geometry
result = (
    cq.Workplane("XY")
    # Create the bottom hexagonal base
    .polygon(nSides=6, diameter=hex_circum_diameter)
    .extrude(hex_thickness)
    
    # Create the central cylindrical shaft
    .faces(">Z").workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
    
    # Create the top hexagonal cap
    .faces(">Z").workplane()
    .polygon(nSides=6, diameter=hex_circum_diameter)
    .extrude(hex_thickness)
)