import cadquery as cq

# Define parameters for the hollow cylinder
height = 100.0       # Total height of the tube
outer_diameter = 30.0 # Outer diameter of the tube
wall_thickness = 5.0  # Thickness of the tube wall

# Calculate inner diameter based on wall thickness
inner_diameter = outer_diameter - (2 * wall_thickness)

# Create the hollow cylinder
# Method: Create a solid cylinder and cut a smaller cylinder from it
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(height)
)

# Alternative method using tube operation if available or preferred for clarity:
# result = cq.Workplane("XY").circle(outer_diameter/2).extrude(height).faces(">Z").hole(inner_diameter)