import cadquery as cq

# Parametric dimensions based on visual estimation
hex_circum_diameter = 14.0  # Corner-to-corner distance of the hexagon
hex_height = 25.0           # Height of the hexagonal section
cyl_diameter = 7.0          # Diameter of the bottom cylinder
cyl_height = 10.0           # Height of the bottom cylinder

# Create the hexagonal prism base on the XY plane and extrude up
# Then select the bottom face to create the cylindrical stem
result = (
    cq.Workplane("XY")
    .polygon(nSides=6, diameter=hex_circum_diameter)
    .extrude(hex_height)
    .faces("<Z")            # Select the bottom face (lowest Z)
    .workplane()            # Create a workplane on the bottom face (normal points -Z)
    .circle(cyl_diameter / 2.0)
    .extrude(cyl_height)    # Extrude along the normal of the selected face (downwards)
)