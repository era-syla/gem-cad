import cadquery as cq

# Parametric dimensions
outer_diameter = 10.0  # Diameter of the tube
wall_thickness = 1.0   # Thickness of the tube wall
length = 100.0         # Length of the tube

# Create the hollow tube
# We create a solid cylinder first
result = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(length)

# Then we create a hole or shell it. 
# Method 1: Create two circles and extrude (more direct)
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle((outer_diameter / 2.0) - wall_thickness)
    .extrude(length)
)

# Alternatively, if it is just a solid rod (which is hard to distinguish definitively 
# without a wireframe or section view, but "tube" is a safe parametric assumption):
# If interpreted as a solid rod:
# result = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(length)

# Given the dark shading on the end face, it strongly suggests a hollow interior.
# I will proceed with the hollow tube code as it is more versatile.

# Final geometry
# Redefining for clarity using the subtractive method which is often cleaner to read
base_rod = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(length)
inner_cut = cq.Workplane("XY").circle((outer_diameter - 2 * wall_thickness) / 2.0).extrude(length)

# This boolean cut is robust
result = base_rod.cut(inner_cut)

# However, the single-step extrusion of a ring is the most "CadQuery" idiomatic way
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle((outer_diameter - 2 * wall_thickness) / 2.0)
    .extrude(length)
)