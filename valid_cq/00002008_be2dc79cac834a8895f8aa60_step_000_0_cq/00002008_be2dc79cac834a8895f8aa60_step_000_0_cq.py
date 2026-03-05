import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
body_diameter = 40.0
body_height = 60.0

# Lip/Rim dimensions (the ring just below the cap)
lip_diameter = 44.0
lip_height = 5.0

# Cap dimensions
cap_diameter = 42.0  # Slightly larger than body, maybe smaller than lip
cap_height = 10.0

# Wall thickness (assuming it's a hollow container)
wall_thickness = 1.5

# --- Modeling ---

# 1. Create the main cylindrical body
# We start from the bottom and work up
main_body = cq.Workplane("XY").circle(body_diameter / 2.0).extrude(body_height)

# 2. Create the lip/rim near the top
# Position: The lip is usually located just below where the cap sits. 
# Based on the image, let's place it at the top of the main body cylinder, 
# and then the cap sits on top of that (or slightly overlaps).
# Let's assume the lip is an integrated part of the bottle neck.
lip = (
    cq.Workplane("XY")
    .workplane(offset=body_height - lip_height)  # Start somewhat below the top
    .circle(lip_diameter / 2.0)
    .extrude(lip_height)
)

# 3. Create the Cap
# The cap sits on top. In a real-world scenario, this might be a separate part,
# but for a single-body visual representation, we stack it.
# The image shows the cap starting right where the lip ends or slightly above.
cap = (
    cq.Workplane("XY")
    .workplane(offset=body_height)
    .circle(cap_diameter / 2.0)
    .extrude(cap_height)
)

# 4. Combine parts
# Union the body and the lip first.
bottle_shape = main_body.union(lip).union(cap)

# 5. Optional: Fillets/Chamfers to match the smooth look
# The top edge of the cap looks sharp, but the transition from lip to body might have a small fillet.
# The bottom edge looks sharp.
# Let's apply a small fillet to the top edge of the cap for realism.
result = bottle_shape.edges(">Z").fillet(0.5)

# If this is intended to be a hollow container, we would shell it, 
# but the image shows a closed assembly (bottle + cap). 
# We will leave it as a solid representation of the assembly.

# Export or display
# show_object(result)