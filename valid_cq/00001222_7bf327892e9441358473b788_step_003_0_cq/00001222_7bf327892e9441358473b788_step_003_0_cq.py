import cadquery as cq

# Define parametric dimensions
outer_diameter = 100.0  # Outer diameter of the ring
height = 30.0           # Height of the ring
thickness = 2.0         # Wall thickness of the ring

# Calculate inner radius based on outer diameter and thickness
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - thickness

# Create the hollow cylinder (ring)
# Method 1: Create a solid cylinder and cut a hole
# result = cq.Workplane("XY").circle(outer_radius).extrude(height).faces(">Z").hole(inner_radius * 2)

# Method 2: Draw concentric circles and extrude (more robust for thin walls)
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)