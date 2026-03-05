import cadquery as cq

# Parametric dimensions
outer_diameter = 50.0  # Outer diameter of the tube
height = 60.0          # Height of the tube
wall_thickness = 5.0   # Thickness of the tube wall

# Derived dimensions
inner_diameter = outer_diameter - (2 * wall_thickness)

# Create the hollow cylinder (tube)
# We create a solid cylinder first, then cut a smaller cylinder from it.
# Alternatively, we can sketch two circles and extrude them.

# Method 1: Boolean cut
# outer_cyl = cq.Workplane("XY").circle(outer_diameter / 2).extrude(height)
# inner_cyl = cq.Workplane("XY").circle(inner_diameter / 2).extrude(height)
# result = outer_cyl.cut(inner_cyl)

# Method 2: Sketching concentric circles and extruding (cleaner)
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)  # Outer circle
    .circle(inner_diameter / 2)  # Inner circle to define the hole
    .extrude(height)
)

# Optional: Export to STL for verification
# cq.exporters.export(result, "tube.stl")