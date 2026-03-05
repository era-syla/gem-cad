import cadquery as cq

# Parametric dimensions
outer_diameter = 50.0  # Diameter of the outer cylinder
inner_diameter = 30.0  # Diameter of the inner hole
height = 60.0          # Height of the cylinder

# Create the hollow cylinder
# Method: Create a solid cylinder and cut a smaller cylinder through it
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(height)
    .faces(">Z")
    .workplane()
    .hole(inner_diameter)
)

# Alternative method using tube/pipe logic directly if preferred:
# result = cq.Workplane("XY").circle(outer_diameter/2).circle(inner_diameter/2).extrude(height)

# The result variable is required by the prompt
part = result