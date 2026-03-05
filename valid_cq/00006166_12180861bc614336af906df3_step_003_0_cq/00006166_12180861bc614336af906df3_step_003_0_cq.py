import cadquery as cq

# Parametric dimensions for a standard washer
# Adjust these values as needed for specific washer sizes (e.g., M10, M12)
outer_diameter = 30.0  # Diameter of the outer circle
inner_diameter = 15.0  # Diameter of the inner hole
thickness = 3.0        # Thickness of the washer

# Create the washer geometry
# 1. Start a sketch on the XY plane
# 2. Draw the outer circle
# 3. Draw the inner circle
# 4. Extrude the sketch to the specified thickness
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(thickness)
)