import cadquery as cq

# Parametric dimensions
cylinder_diameter = 50.0  # Diameter of the cylinder
cylinder_height = 50.0    # Total height of the cylinder
fillet_radius = 5.0       # Radius of the fillet on top and bottom edges

# Create the base cylinder
# We center it on X and Y, and align the base with Z=0 for easier mental modeling,
# though centering on Z is also a common practice.
base = cq.Workplane("XY").circle(cylinder_diameter / 2.0).extrude(cylinder_height)

# Apply fillets to the top and bottom edges
# We select edges based on the "Z" direction (top and bottom faces) or just select all circular edges
result = base.edges().fillet(fillet_radius)

# Optional: If you wanted to be very specific about selecting top and bottom edges only:
# result = base.edges(">Z or <Z").fillet(fillet_radius)

# The result variable now contains the final geometry