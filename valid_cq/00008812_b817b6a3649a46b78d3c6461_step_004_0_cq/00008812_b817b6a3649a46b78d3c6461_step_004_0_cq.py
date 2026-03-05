import cadquery as cq
from math import sin, cos, radians, pi

# --- Parameters ---
main_diameter = 20.0
thickness = 8.0
scallop_radius = 1.0  # Radius of the small circles on the edge
num_scallops = 40     # Number of scallops around the perimeter
indent_diameter = 8.0 # Diameter of the spherical indentation
indent_offset = 5.0   # Distance from center to the indentation center

# --- Derived Dimensions ---
main_radius = main_diameter / 2.0
# Calculate the radius where the scallops are centered so they touch/merge nicely
scallop_center_radius = main_radius

# --- Modeling ---

# 1. Create the main cylindrical body
base = cq.Workplane("XY").circle(main_radius).extrude(thickness)

# 2. Create the scalloped edge
# We will create a series of cylinders arranged in a circle and union them with the base.
# Alternatively, we can sketch the entire profile at once, but unioning is often simpler for patterns.
scallops = (
    cq.Workplane("XY")
    .polarArray(scallop_center_radius, 0, 360, num_scallops)
    .circle(scallop_radius)
    .extrude(thickness)
)

# Union the scallops with the base cylinder
knob_body = base.union(scallops)

# 3. Create the spherical indentation
# We create a sphere and cut it away from the top face
indent_sphere = (
    cq.Workplane("XY")
    .workplane(offset=thickness)  # Start at the top surface
    .center(indent_offset, 0)     # Move to the offset position
    .sphere(indent_diameter / 2.0)
)

# Cut the sphere from the main body
result = knob_body.cut(indent_sphere)

# Export or visualization helper (not strictly required by prompt but good practice)
# cq.exporters.export(result, "knob.step")