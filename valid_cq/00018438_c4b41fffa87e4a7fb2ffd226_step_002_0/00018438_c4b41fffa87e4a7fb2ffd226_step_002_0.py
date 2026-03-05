import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
base_diameter = 100.0   # Diameter of the large circular disc
base_thickness = 2.0    # Thickness of the disc
pin_diameter = 3.0      # Diameter of the central pin
pin_height = 8.0        # Height of the pin protruding from the surface

# Create the base disc
# 1. Start on the XY plane
# 2. Draw the base circle
# 3. Extrude to create the thickness
result = (
    cq.Workplane("XY")
    .circle(base_diameter / 2.0)
    .extrude(base_thickness)
)

# Add the central pin
# 1. Select the top face of the existing disc (direction >Z)
# 2. Create a new workplane on that face
# 3. Draw the pin circle at the center
# 4. Extrude the pin upwards
result = (
    result.faces(">Z")
    .workplane()
    .circle(pin_diameter / 2.0)
    .extrude(pin_height)
)