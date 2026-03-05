import cadquery as cq

# Parametric dimensions
length = 100.0   # Length of the tube
outer_diam = 10.0 # Outer diameter of the tube
wall_thickness = 2.0 # Wall thickness of the tube

# Derived dimensions
outer_radius = outer_diam / 2.0
inner_radius = outer_radius - wall_thickness

# Generate the geometry
# Method 1: Create a solid cylinder and cut a hole
# result = cq.Workplane("XY").circle(outer_radius).extrude(length).faces(">Z").hole(inner_radius * 2)

# Method 2: Create a sketch with two circles and extrude (more robust for pipes)
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(length)
)

# Alternatively, using the tube function if available in specific contexts, 
# but the circle-circle-extrude method is the most standard CadQuery way for a pipe.