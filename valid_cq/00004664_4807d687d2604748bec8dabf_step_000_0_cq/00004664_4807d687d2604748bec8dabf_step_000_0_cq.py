import cadquery as cq

# Parametric dimensions for a standard washer
# These values can be adjusted to create specific washer sizes (e.g., M10, M12)
outer_diameter = 30.0  # The external diameter of the washer
inner_diameter = 16.0  # The internal hole diameter
thickness = 3.0        # The thickness of the washer

# Create the washer geometry
# Method 1: Create a solid cylinder and cut a hole
# result = cq.Workplane("XY").circle(outer_diameter / 2).extrude(thickness) \
#            .faces(">Z").workplane().hole(inner_diameter)

# Method 2: Create a 2D profile with a hole and extrude it (often cleaner)
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)  # Outer circle
    .circle(inner_diameter / 2)  # Inner circle (creates the hole in the sketch)
    .extrude(thickness)          # Extrude the ring profile
)

# Export the result (optional, but good practice for verification)
# cq.exporters.export(result, "washer.step")