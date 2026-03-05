import cadquery as cq

# Parameters for the tube
height = 50.0       # Total height of the cylinder
outer_radius = 20.0 # Outer radius of the tube
wall_thickness = 2.0 # Thickness of the wall

# Calculated parameter
inner_radius = outer_radius - wall_thickness

# Create the hollow cylinder (tube)
# Method 1: Create a solid cylinder and cut a smaller one from it
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(height)
    .faces(">Z")
    .workplane()
    .hole(inner_radius * 2)
)

# Alternative simpler method:
# result = cq.Workplane("XY").circle(outer_radius).circle(inner_radius).extrude(height)