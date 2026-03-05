import cadquery as cq

# Parametric dimensions
hex_circum_diameter = 12.0  # Diameter of the circle circumscribing the hexagon
base_thickness = 6.0        # Height of the hexagonal base
shaft_diameter = 7.0        # Diameter of the cylindrical section
shaft_height = 24.0         # Height of the cylindrical section
hole_diameter = 3.0         # Diameter of the central through-hole

# Generate the 3D model
result = (
    cq.Workplane("XY")
    # Create the hexagonal base
    .polygon(nSides=6, diameter=hex_circum_diameter)
    .extrude(base_thickness)
    
    # Create the cylindrical shaft on top of the base
    .faces(">Z").workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_height)
    
    # Create the central hole through the entire assembly
    .faces(">Z").workplane()
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)