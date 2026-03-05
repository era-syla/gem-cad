import cadquery as cq

# --- Parametric Dimensions ---
outer_diameter = 50.0   # Diameter of the outer circle
inner_diameter = 30.0   # Diameter of the inner hole
thickness = 8.0         # Height/thickness of the ring
fillet_radius = 2.0     # Radius of the edge fillets

# --- Modeling ---

# 1. Create the base washer shape (cylinder with a hole)
# We extrude a sketch or just use primitive operations.
# Using a sketch is often cleaner for parametric workflows.
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(thickness)
)

# 2. Apply fillets to the top edges
# We select edges on the top face (">Z")
# The selector will grab both the inner and outer circular edges on the top face.
result = result.edges(">Z").fillet(fillet_radius)

# Note: The bottom edges in the image appear sharp, but if symmetry was desired,
# one could select edges on "<Z" as well. Based on the single view, 
# only top fillets are clearly visible.