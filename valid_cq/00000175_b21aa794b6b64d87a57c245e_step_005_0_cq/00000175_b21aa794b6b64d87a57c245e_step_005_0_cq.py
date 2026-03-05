import cadquery as cq

# Parametric dimensions for a standard flat washer (e.g., M10 size)
# You can adjust these values to change the size of the washer
outer_diameter = 20.0  # Diameter of the outer circle
inner_diameter = 10.5  # Diameter of the inner hole
thickness = 2.0        # Thickness of the washer

# Create the washer geometry
# 1. Start a workplane on the XY plane
# 2. Draw the outer circle
# 3. Draw the inner circle
# 4. Extrude the sketch to the specified thickness
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(thickness)
)

# The 'result' variable now contains the CadQuery object representing the washer