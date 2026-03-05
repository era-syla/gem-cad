import cadquery as cq

# Parametric dimensions
outer_diameter = 50.0  # Outer diameter of the washer/spacer
inner_diameter = 30.0  # Inner diameter of the hole
height = 15.0          # Thickness/height of the cylinder

# Create the washer geometry
# Method: Create a solid cylinder and cut a smaller cylinder from it
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(height)
    .faces(">Z")
    .workplane()
    .hole(inner_diameter)
)

# Alternative method (often cleaner for simple tubes):
# result = cq.Workplane("XY").circle(outer_diameter/2).circle(inner_diameter/2).extrude(height)