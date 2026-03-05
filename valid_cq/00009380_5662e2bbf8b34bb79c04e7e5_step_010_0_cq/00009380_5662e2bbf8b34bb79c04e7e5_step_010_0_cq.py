import cadquery as cq

# --- Parametric Dimensions ---
# Outer dimensions of the main wheel
wheel_outer_diameter = 50.0
wheel_width = 25.0

# Hub dimensions (the central protruding part)
hub_diameter = 20.0
hub_protrusion = 3.0  # How much it sticks out from the main face on one side

# Axle/Bore dimensions
bore_diameter = 10.0

# Aesthetic details
chamfer_size = 2.0  # Chamfer on the outer edge of the wheel
fillet_size = 1.0   # Fillet where the hub meets the wheel face

# --- Modeling Process ---

# 1. Create the main cylindrical body of the wheel
# We create a cylinder centered at the origin
main_body = cq.Workplane("XY").circle(wheel_outer_diameter / 2.0).extrude(wheel_width)

# 2. Add chamfers to the outer edges
# We select the faces at Z=0 and Z=width, then their outer wires
main_body = main_body.faces(">Z or <Z").edges().chamfer(chamfer_size)

# 3. Create the hub
# The hub needs to stick out from the center.
# In the image, it looks like there might be a hub on both sides, or at least one visible side.
# Let's assume a symmetrical design where the hub protrudes from both sides for a generic wheel,
# or we can model it just on the front face as seen.
# Based on the visible perspective, let's add it to the front face (>Z) and cut the back to match or add it to both.
# Let's go with a symmetrical hub design as is common for this type of roller.

# We will create a cylinder that goes through the whole wheel + protrusion on both sides
total_hub_length = wheel_width + (2 * hub_protrusion)

# Create the hub cylinder centered on the existing geometry
hub = (
    cq.Workplane("XY")
    .workplane(offset=-hub_protrusion) # Start slightly below the main body
    .circle(hub_diameter / 2.0)
    .extrude(total_hub_length)
)

# Combine the main body and the hub
result = main_body.union(hub)

# 4. Add fillets where the hub meets the main wheel face
# We need to select the edges at the intersection. 
# These are circles on the faces of the original wheel width.
# A robust way is to select edges on the 'hub' cylinder that are within the Z range of the faces.
# Alternatively, select edges near the Z-face planes.
result = result.edges(cq.selectors.RadiusNthSelector(1)).fillet(fillet_size)

# 5. Cut the central bore hole
result = result.faces(">Z").workplane().hole(bore_diameter)

# Return the final geometry
# (The variable 'result' is required by the prompt)