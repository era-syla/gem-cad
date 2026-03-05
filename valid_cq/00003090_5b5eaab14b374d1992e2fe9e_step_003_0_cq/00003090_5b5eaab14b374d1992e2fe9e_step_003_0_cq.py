import cadquery as cq

# Parametric dimensions
head_diameter = 20.0  # Diameter of the wider head section
head_height = 4.0     # Thickness of the head
body_diameter = 16.0  # Diameter of the main cylindrical body
body_length = 20.0    # Length of the main body
top_fillet = 1.0      # Fillet radius on the top edge of the head
bottom_chamfer = 1.0  # Chamfer size on the bottom edge of the body

# Create the main body
# Start with a sketch on the XY plane
result = (
    cq.Workplane("XY")
    # Draw the main body cylinder circle
    .circle(body_diameter / 2)
    # Extrude it to the body length
    .extrude(body_length)
)

# Create the head
# Select the bottom face of the existing cylinder (at Z=0) to add material downwards
# or select the top face (at Z=body_length) if we want the head there.
# Looking at the image, let's assume the "head" is at the base (Z=0) and we extruded up.
# So let's build the head on the "bottom" face (Z=0 plane basically) but going in the negative direction
# Or, simpler: Create the head first, then the body on top.

# Let's start over with a cleaner stacked approach: Head then Body.

result = (
    cq.Workplane("XY")
    # 1. Create the Head
    .circle(head_diameter / 2)
    .extrude(head_height)
    
    # 2. Create the Body on top of the Head
    .faces(">Z") # Select the top face of the head
    .workplane()
    .circle(body_diameter / 2)
    .extrude(body_length)
)

# Apply finishing features (Fillets and Chamfers) based on the visual
# The top of the head (the transition to the body) seems to have a small fillet or just a sharp corner. 
# In the image, the very "top" (the large flat face of the head, viewed from bottom-left) looks rounded.
# The "end" of the pin (the small face, right side) has a chamfer.

# Let's refine the orientation to match the image better:
# The image shows a large flange/head on the left, and the cylinder extending to the right.
# Let's apply a fillet to the outer edge of the head.
result = result.edges("<Z").fillet(top_fillet) # Fillet the bottom-most edge (the outer face of the head)

# Apply chamfer to the end of the pin
result = result.edges(">Z").chamfer(bottom_chamfer)

# Optional: There might be a small fillet between the head and the body for stress relief
# result = result.edges(cq.selectors.NearestToPointSelector((0,0, head_height))).fillet(0.5)

# Final check of the generated geometry
# It consists of a cylinder with a larger cylindrical base (flange/head), 
# a fillet on the head's outer face, and a chamfer on the tip.