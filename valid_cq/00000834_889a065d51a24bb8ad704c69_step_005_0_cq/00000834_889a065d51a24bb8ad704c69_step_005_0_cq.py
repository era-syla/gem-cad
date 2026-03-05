import cadquery as cq

# --- Parametric Dimensions ---
outer_diameter = 10.0   # Diameter of the cylinder
total_length = 80.0     # Length of the cylinder
hole_diameter = 2.0     # Diameter of the through-hole

# --- Modeling ---
# Create the main cylinder
# We construct a cylinder on the XY plane extending along the Z axis
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(total_length)
    # Create the hole
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)
)

# Alternatively, a more direct way for a simple tube:
# result = cq.Workplane("XY").circle(outer_diameter / 2).circle(hole_diameter / 2).extrude(total_length)

# The result variable now contains the final geometry