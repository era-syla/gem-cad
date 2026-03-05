import cadquery as cq

# Parametric dimensions
length = 100.0  # Length of the box
width = 60.0    # Width of the box
height = 50.0   # Total height of the box
fillet_radius = 10.0 # Radius of the top edge fillet

# Create the base block
# We create a box centered on X and Y, but sitting on the Z plane (Z=0 to Z=height)
box = cq.Workplane("XY").box(length, width, height)

# Apply fillet to the top edges
# We select the face in the Z direction (top face) and get its outer edges
result = box.faces("+Z").edges().fillet(fillet_radius)