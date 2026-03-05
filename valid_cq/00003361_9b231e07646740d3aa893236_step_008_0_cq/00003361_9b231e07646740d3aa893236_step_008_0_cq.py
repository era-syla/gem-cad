import cadquery as cq

# Parametric dimensions
length = 200.0  # Length of the tube
outer_diameter = 10.0  # Outer diameter of the tube
wall_thickness = 1.5   # Thickness of the tube wall

# Calculate inner diameter
inner_diameter = outer_diameter - (2 * wall_thickness)

# Create the tube
# We create a solid cylinder first
result = cq.Workplane("XY").circle(outer_diameter / 2).extrude(length)

# Then cut the inner hole to make it a tube
# We could also do this in one step by drawing two circles and extruding, 
# but a cut operation is often more explicit for "drilling" operations.
# Alternatively, drawing concentric circles on the sketch is cleaner.

result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(length)
)

# Optional: Add small fillets to the ends for a more realistic look
# result = result.faces("<Z or >Z").edges().fillet(0.2)

# The result variable is required
result = result